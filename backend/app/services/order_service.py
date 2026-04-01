from datetime import UTC, datetime
from uuid import uuid4

from fastapi import HTTPException
from sqlalchemy.orm import Session, joinedload

from app.models.order import Order, OrderStatus
from app.models.order_item import OrderItem
from app.models.product import Product
from app.models.user import User
from app.schemas.order import OrderCreate


def _generate_order_number() -> str:
    timestamp = datetime.now(UTC).strftime("%Y%m%d%H%M%S")
    random_part = uuid4().hex[:8].upper()
    return f"ORD-{timestamp}-{random_part}"


def create_order(data: OrderCreate, current_user: User, db: Session) -> Order:
    product_ids = [item.product_id for item in data.items]

    aggregated_quantities: dict[int, int] = {}
    for item in data.items:
        aggregated_quantities[item.product_id] = (
            aggregated_quantities.get(item.product_id, 0) + item.quantity
        )

    products = (
        db.query(Product)
        .filter(Product.id.in_(product_ids))
        .with_for_update()
        .all()
    )
    products_by_id = {product.id: product for product in products}

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

    insufficient_stock_items: list[str] = []
    for product_id, needed_quantity in aggregated_quantities.items():
        product = products_by_id[product_id]
        if product.stock < needed_quantity:
            insufficient_stock_items.append(
                f"{product.name} (requested {needed_quantity}, available {product.stock})"
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
    for item in data.items:
        product = products_by_id[item.product_id]
        unit_price = product.price
        line_total = unit_price * item.quantity

        order.items.append(
            OrderItem(
                product_id=product.id,
                product_name=product.name,
                quantity=item.quantity,
                unit_price=unit_price,
                line_total=line_total,
            )
        )
        total_price += line_total

    for product_id, needed_quantity in aggregated_quantities.items():
        product = products_by_id[product_id]
        product.stock -= needed_quantity

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
