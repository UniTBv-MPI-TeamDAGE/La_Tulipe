from uuid import uuid4

from fastapi.testclient import TestClient

from app.database.db import SessionLocal
from app.main import app
from app.models.category import Category
from app.models.order import Order
from app.models.product import Product, ProductSeason, ProductType
from app.models.user import User

client = TestClient(app)


def _register_and_login_user() -> tuple[str, str]:
    email = f"order_{uuid4().hex[:8]}@test.com"
    password = "12345678"

    register_response = client.post(
        "/api/auth/register",
        json={
            "name": "Order Customer",
            "email": email,
            "password": password,
            "confirm_password": password,
        },
    )
    assert register_response.status_code == 201

    login_response = client.post(
        "/api/auth/login",
        json={
            "email": email,
            "password": password,
        },
    )
    assert login_response.status_code == 200
    token = login_response.json()["access_token"]

    return email, token


def test_create_order_valid_returns_201_and_decrements_stock():
    db = SessionLocal()
    user_email, token = _register_and_login_user()
    category = Category(name="Order Test Category")
    db.add(category)
    db.commit()
    db.refresh(category)

    product = Product(
        name="Order Test Rose",
        description="Rose used for order test",
        price=10.0,
        stock=5,
        image_url=None,
        is_featured=False,
        season=ProductSeason.ALL_SEASON,
        product_type=ProductType.INDIVIDUAL,
        category_id=category.id,
    )
    db.add(product)
    db.commit()
    db.refresh(product)

    try:
        response = client.post(
            "/api/orders",
            headers={"Authorization": f"Bearer {token}"},
            json={
                "customer_name": "Ana Pop",
                "customer_email": "ana.order@test.com",
                "customer_phone": "0712345678",
                "delivery_address": "Strada Florilor 10, Bucuresti",
                "card_message": "La multi ani!",
                "items": [{"product_id": product.id, "quantity": 3}],
            },
        )

        assert response.status_code == 201
        data = response.json()
        assert data["order_number"].startswith("ORD-")
        assert data["status"] == "pending"
        assert data["total_price"] == 30.0
        assert len(data["items"]) == 1
        assert data["items"][0]["product_id"] == product.id
        assert data["items"][0]["quantity"] == 3
        assert data["items"][0]["unit_price"] == 10.0
        assert data["items"][0]["line_total"] == 30.0

        db.refresh(product)
        assert product.stock == 2
    finally:
        user = db.query(User).filter(User.email == user_email).first()
        db.query(Order).delete()
        db.delete(product)
        db.delete(category)
        if user:
            db.delete(user)
        db.commit()
        db.close()


def test_create_order_insufficient_stock_returns_409():
    db = SessionLocal()
    user_email, token = _register_and_login_user()
    category = Category(name="Order Stock Category")
    db.add(category)
    db.commit()
    db.refresh(category)

    product = Product(
        name="Low Stock Tulip",
        description="Tulip used for low stock test",
        price=12.0,
        stock=1,
        image_url=None,
        is_featured=False,
        season=ProductSeason.SPRING,
        product_type=ProductType.INDIVIDUAL,
        category_id=category.id,
    )
    db.add(product)
    db.commit()
    db.refresh(product)

    try:
        response = client.post(
            "/api/orders",
            headers={"Authorization": f"Bearer {token}"},
            json={
                "customer_name": "Mara Ionescu",
                "customer_email": "mara.order@test.com",
                "customer_phone": "0722334455",
                "delivery_address": "Strada Lalelelor 5, Cluj",
                "items": [{"product_id": product.id, "quantity": 2}],
            },
        )

        assert response.status_code == 409
        assert "Insufficient stock" in response.json()["detail"]

        db.refresh(product)
        assert product.stock == 1
    finally:
        user = db.query(User).filter(User.email == user_email).first()
        db.query(Order).delete()
        db.delete(product)
        db.delete(category)
        if user:
            db.delete(user)
        db.commit()
        db.close()


def test_create_order_without_auth_returns_401():
    response = client.post(
        "/api/orders",
        json={
            "customer_name": "Guest User",
            "customer_email": "guest@test.com",
            "customer_phone": "0711111111",
            "delivery_address": "No Auth Street 1",
            "items": [{"product_id": 1, "quantity": 1}],
        },
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Unauthorized"
