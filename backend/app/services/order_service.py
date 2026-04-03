from datetime import UTC, datetime
from uuid import uuid4

from fastapi import HTTPException
from sqlalchemy.orm import Session, joinedload

from app.models.color import Color
from app.models.order import Order, OrderStatus
from app.models.order_item import OrderItem
from app.models.product import Product, ProductColorStock
from app.models.user import User
from app.schemas.order import OrderCreate


def _generate_order_number() -> str:
    timestamp = datetime.now(UTC).strftime("%Y%m%d%H%M%S")
    random_part = uuid4().hex[:8].upper()
    return f"ORD-{timestamp}-{random_part}"


def create_order(data: OrderCreate, current_user: User, db: Session) -> Order:
    product_ids = [item.product_id for item in data.items]

    aggregated_default_stock: dict[int, int] = {}
    aggregated_color_stock: dict[tuple[int, int], int] = {}

    products = (
        db.query(Product)
        .filter(Product.id.in_(product_ids))
        .with_for_update()
        .all()
    )
    products_by_id = {product.id: product for product in products}

    product_color_stocks = (
        db.query(ProductColorStock)
        .filter(ProductColorStock.product_id.in_(product_ids))
        .with_for_update()
        .all()
    )
    color_ids = sorted({item.color_id for item in product_color_stocks})
    colors_by_id = {
        color.id: color
        for color in db.query(Color).filter(Color.id.in_(color_ids)).all()
    }
    color_stock_by_key = {
        (item.product_id, item.color_id): item for item in product_color_stocks
    }
    has_color_stocks_by_product_id = {
        item.product_id for item in product_color_stocks
    }

    missing_product_ids = [
        product_id
        for product_id in sorted(set(product_ids))
        if product_id not in products_by_id
    ]
    if missing_product_ids:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid product ids: {missing_product_ids}",
        )

    resolved_items: list[tuple[object, Product, ProductColorStock | None]] = []
    for item in data.items:
        product = products_by_id[item.product_id]

        if product.id in has_color_stocks_by_product_id:
            if item.color_id is None:
                raise HTTPException(
                    status_code=400,
                    detail=f"Color is required for product '{product.name}'",
                )

            color_stock = color_stock_by_key.get((product.id, item.color_id))
            if not color_stock:
                raise HTTPException(
                    status_code=400,
                    detail=(
                        f"Invalid color '{item.color_id}' "
                        f"for product '{product.name}'"
                    ),
                )

            aggregated_color_stock[(product.id, item.color_id)] = (
                aggregated_color_stock.get((product.id, item.color_id), 0)
                + item.quantity
            )
            resolved_items.append((item, product, color_stock))
        else:
            if item.color_id is not None:
                raise HTTPException(
                    status_code=400,
                    detail=(
                        f"Product '{product.name}' does not support color-specific stock"
                    ),
                )

            aggregated_default_stock[product.id] = (
                aggregated_default_stock.get(product.id, 0) + item.quantity
            )
            resolved_items.append((item, product, None))

    insufficient_stock_items: list[str] = []

    for product_id, needed_quantity in aggregated_default_stock.items():
        product = products_by_id[product_id]
        if product.stock < needed_quantity:
            insufficient_stock_items.append(
                (
                    f"{product.name} (requested {needed_quantity}, "
                    f"available {product.stock})"
                )
            )

    for (product_id, color_id), needed_quantity in aggregated_color_stock.items():
        color_stock = color_stock_by_key[(product_id, color_id)]
        color_name = colors_by_id.get(color_id).name if colors_by_id.get(color_id) else str(color_id)
        product_name = products_by_id[product_id].name
        if color_stock.stock < needed_quantity:
            insufficient_stock_items.append(
                (
                    f"{product_name} - {color_name} "
                    f"(requested {needed_quantity}, available {color_stock.stock})"
                )
            )

    if insufficient_stock_items:
        raise HTTPException(
            status_code=409,
            detail=(
                "Insufficient stock for: "
                + ", ".join(insufficient_stock_items)
            ),
        )

    order = Order(
        order_number=_generate_order_number(),
        user_id=current_user.id,
        customer_name=data.customer_name,
        customer_email=str(data.customer_email),
        customer_phone=data.customer_phone,
        delivery_address=data.delivery_address,
        card_message=data.card_message,
        status=OrderStatus.PENDING,
        total_price=0,
    )

    total_price = 0.0
    for item, product, color_stock in resolved_items:
        unit_price = product.price
        line_total = unit_price * item.quantity

        order.items.append(
            OrderItem(
                product_id=product.id,
                product_name=product.name,
                color_id=color_stock.color_id if color_stock else None,
                color_name=(
                    colors_by_id.get(color_stock.color_id).name
                    if color_stock and colors_by_id.get(color_stock.color_id)
                    else None
                ),
                quantity=item.quantity,
                unit_price=unit_price,
                line_total=line_total,
            )
        )
        total_price += line_total

    for product_id, needed_quantity in aggregated_default_stock.items():
        product = products_by_id[product_id]
        product.stock -= needed_quantity

    for (product_id, color_id), needed_quantity in aggregated_color_stock.items():
        color_stock = color_stock_by_key[(product_id, color_id)]
        color_stock.stock -= needed_quantity

    order.total_price = total_price

    db.add(order)
    db.commit()
    db.refresh(order)

    return (
        db.query(Order)
        .options(joinedload(Order.items))
        .filter(Order.id == order.id)
        .first()
    )


def get_my_orders(current_user: User, db: Session) -> list[Order]:
    return (
        db.query(Order)
        .options(joinedload(Order.items))
        .filter(Order.user_id == current_user.id)
        .order_by(Order.created_at.desc(), Order.id.desc())
        .all()
    )


def get_my_order_or_404(order_id: int, current_user: User, db: Session) -> Order:
    order = (
        db.query(Order)
        .options(joinedload(Order.items))
        .filter(Order.id == order_id, Order.user_id == current_user.id)
        .first()
    )
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    return order
