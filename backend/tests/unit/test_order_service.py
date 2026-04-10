from unittest.mock import MagicMock

import pytest
from fastapi import HTTPException

from app.models.order import Order, OrderStatus
from app.models.product import Product
from app.models.user import User
from app.schemas.order import OrderCreate
from app.services.order_service import (
    create_order,
    get_my_order_or_404,
    get_my_orders,
    update_order_status_for_admin,
)


def make_order_data(items):
    return OrderCreate(
        customer_name="Ana",
        customer_email="ana@test.com",
        customer_phone="0712345678",
        delivery_address="Strada X",
        card_message=None,
        items=items
    )

def test_create_order_invalid_product():
    db = MagicMock()
    user = User(id=1)

    db.query().filter().with_for_update().all.return_value = []

    data = make_order_data([
        {"product_id": 999, "quantity": 1}
    ])

    with pytest.raises(HTTPException):
        create_order(data, user, db)


def test_create_order_insufficient_stock():
    db = MagicMock()
    user = User(id=1)

    product = Product(id=1, name="Rose", stock=1, price=10)

    db.query().filter().with_for_update().all.return_value = [product]
    db.query().filter().with_for_update().all.side_effect = [
        [product], 
        [],         
    ]

    data = make_order_data([
        {"product_id": 1, "quantity": 5}
    ])

    with pytest.raises(HTTPException) as e:
        create_order(data, user, db)

    assert e.value.status_code == 409

def test_create_order_missing_color():
    db = MagicMock()
    user = User(id=1)

    product = Product(id=1, name="Rose", stock=10, price=10)

    color_stock = MagicMock(product_id=1, color_id=1)

    db.query().filter().with_for_update().all.side_effect = [
        [product],         
        [color_stock],    
    ]

    data = make_order_data([
        {"product_id": 1, "quantity": 1}  
    ])

    with pytest.raises(HTTPException):
        create_order(data, user, db)
        
        
def test_create_order_success():
    db = MagicMock()
    user = User(id=1)

    product = Product(id=1, name="Rose", stock=10, price=10)

    db.query().filter().with_for_update().all.side_effect = [
        [product],  
        [],         
    ]

    order = Order(id=1)
    db.query().options().filter().first.return_value = order

    data = make_order_data([
        {"product_id": 1, "quantity": 2}
    ])

    result = create_order(data, user, db)

    assert result == order
    db.add.assert_called()
    db.commit.assert_called()


def test_get_my_orders():
    db = MagicMock()
    user = User(id=1)

    orders = [Order(id=1), Order(id=2)]
    db.query().options().filter().order_by().all.return_value = orders

    result = get_my_orders(user, db)

    assert result == orders


def test_get_my_order_not_found():
    db = MagicMock()
    user = User(id=1)

    db.query().options().filter().first.return_value = None

    with pytest.raises(HTTPException):
        get_my_order_or_404(1, user, db)


def test_get_my_order_success():
    db = MagicMock()
    user = User(id=1)

    order = Order(id=1)
    db.query().options().filter().first.return_value = order

    result = get_my_order_or_404(1, user, db)

    assert result == order


def test_update_order_not_found():
    db = MagicMock()

    db.query().options().filter().first.return_value = None

    with pytest.raises(HTTPException):
        update_order_status_for_admin(
            order_id=1,
            new_status=OrderStatus.CONFIRMED,
            db=db
        )


def test_update_order_invalid_transition():
    db = MagicMock()

    order = Order(id=1, status=OrderStatus.CANCELLED)
    db.query().options().filter().first.return_value = order

    with pytest.raises(HTTPException):
        update_order_status_for_admin(
            order_id=1,
            new_status=OrderStatus.CONFIRMED,
            db=db
        )


def test_update_order_success():
    db = MagicMock()

    order = Order(id=1, status=OrderStatus.PENDING)

    db.query().options().filter().first.side_effect = [
        order, 
        order  
    ]

    result = update_order_status_for_admin(
        order_id=1,
        new_status=OrderStatus.CONFIRMED,
        db=db
    )

    assert result.status == OrderStatus.CONFIRMED
    db.commit.assert_called()