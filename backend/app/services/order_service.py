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
    import json

    product_ids_regular = [
        item.product_id for item in data.items 
        if item.product_id is not None and not item.custom_composition
    ]
    product_ids_custom = []
    for item in data.items:
        if item.custom_composition:
            product_ids_custom.extend(
                [comp.product_id for comp in item.custom_composition]
            )

    all_product_ids = sorted(set(product_ids_regular + product_ids_custom))

    aggregated_default_stock: dict[int, int] = {}
    aggregated_color_stock: dict[tuple[int, int], int] = {}

    products = (
        db.query(Product)
        .filter(Product.id.in_(all_product_ids))
        .with_for_update()
        .all()
    )
    products_by_id = {product.id: product for product in products}

    product_color_stocks = (
        db.query(ProductColorStock)
        .filter(ProductColorStock.product_id.in_(all_product_ids))
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
        for product_id in all_product_ids
        if product_id not in products_by_id
    ]
    if missing_product_ids:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid product ids: {missing_product_ids}",
        )

    resolved_items: list[
        tuple[object, Product | None, ProductColorStock | None, dict | None]
    ] = []
    
    for item in data.items:
        if item.custom_composition:
            composition_list = []
            for comp in item.custom_composition:
                product = products_by_id[comp.product_id]
                
                if product.id in has_color_stocks_by_product_id:
                    if comp.color_id is None:
                        raise HTTPException(
                            status_code=400,
                            detail=(
                                "Color is required for "
                                f"'{product.name}' in custom bouquet"
                            ),
                        )

                    color_stock = color_stock_by_key.get((product.id, comp.color_id))
                    if not color_stock:
                        raise HTTPException(
                            status_code=400,
                            detail=(
                                f"Invalid color '{comp.color_id}' "
                                f"for product '{product.name}'"
                            ),
                        )

                    aggregated_color_stock[(product.id, comp.color_id)] = (
                        aggregated_color_stock.get((product.id, comp.color_id), 0)
                        + comp.quantity * item.quantity
                    )
                    color = colors_by_id.get(comp.color_id)
                    composition_list.append(
                        {
                            "product_id": product.id,
                            "product_name": product.name,
                            "color_id": comp.color_id,
                            "color_name": (
                                color.name if color else str(comp.color_id)
                            ),
                            "quantity": comp.quantity,
                        }
                    )
                else:
                    if comp.color_id is not None:
                        raise HTTPException(
                            status_code=400,
                            detail=(
                                f"Product '{product.name}' "
                                "does not support color selection"
                            ),
                        )

                    aggregated_default_stock[product.id] = (
                        aggregated_default_stock.get(product.id, 0)
                        + comp.quantity * item.quantity
                    )
                    composition_list.append({
                        "product_id": product.id,
                        "product_name": product.name,
                        "quantity": comp.quantity,
                    })

            resolved_items.append((item, None, None, composition_list))
        else:
            if item.product_id is None:
                raise HTTPException(
                    status_code=400,
                    detail="product_id required when custom_composition not provided",
                )

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
                resolved_items.append((item, product, color_stock, None))
            else:
                if item.color_id is not None:
                    raise HTTPException(
                        status_code=400,
                        detail=(
                            f"Product '{product.name}' "
                            "does not support color-specific stock"
                        ),
                    )

                aggregated_default_stock[product.id] = (
                    aggregated_default_stock.get(product.id, 0) + item.quantity
                )
                resolved_items.append((item, product, None, None))

    aggregated_total_stock_by_product: dict[int, int] = dict(aggregated_default_stock)
    for (product_id, _color_id), needed_quantity in aggregated_color_stock.items():
        aggregated_total_stock_by_product[product_id] = (
            aggregated_total_stock_by_product.get(product_id, 0) + needed_quantity
        )

    insufficient_stock_items: list[str] = []

    for product_id, needed_quantity in aggregated_total_stock_by_product.items():
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
        color = colors_by_id.get(color_id)
        color_name = color.name if color else str(color_id)
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
    for item, product, color_stock, composition in resolved_items:
        if composition:
            composition_price = 0.0
            for comp in composition:
                comp_product = products_by_id[comp["product_id"]]
                composition_price += comp_product.price * comp["quantity"]
            
            line_total = composition_price * item.quantity
            unit_price = composition_price
            
            order.items.append(
                OrderItem(
                    product_id=None,
                    product_name="Custom Bouquet",
                    color_id=None,
                    color_name=None,
                    quantity=item.quantity,
                    unit_price=unit_price,
                    line_total=line_total,
                    composition=json.dumps(composition),
                )
            )
            total_price += line_total
        else:
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
                    composition=None,
                )
            )
            total_price += line_total

    for product_id, needed_quantity in aggregated_total_stock_by_product.items():
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


ALLOWED_STATUS_TRANSITIONS: dict[OrderStatus, set[OrderStatus]] = {
    OrderStatus.PENDING: {OrderStatus.CONFIRMED, OrderStatus.CANCELLED},
    OrderStatus.CONFIRMED: {OrderStatus.DELIVERED, OrderStatus.CANCELLED},
    OrderStatus.DELIVERED: {OrderStatus.CANCELLED},
    OrderStatus.CANCELLED: set(),
}


def get_all_orders_for_admin(
    *,
    db: Session,
    status: OrderStatus | None = None,
) -> list[Order]:
    query = db.query(Order).options(joinedload(Order.items))
    if status is not None:
        query = query.filter(Order.status == status)

    return query.order_by(Order.created_at.desc(), Order.id.desc()).all()


def update_order_status_for_admin(
    *,
    order_id: int,
    new_status: OrderStatus,
    db: Session,
) -> Order:
    order = db.query(Order).options(joinedload(Order.items)).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    if order.status == new_status:
        return order

    allowed_next_statuses = ALLOWED_STATUS_TRANSITIONS.get(order.status, set())
    if new_status not in allowed_next_statuses:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid status transition: {order.status.value} -> {new_status.value}",
        )

    order.status = new_status
    db.add(order)
    db.commit()
    db.refresh(order)

    return (
        db.query(Order)
        .options(joinedload(Order.items))
        .filter(Order.id == order.id)
        .first()
    )
