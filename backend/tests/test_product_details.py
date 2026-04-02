from fastapi.testclient import TestClient

from app.database.db import SessionLocal
from app.main import app
from app.models.category import Category
from app.models.product import Product, ProductSeason, ProductType

client = TestClient(app)


def test_get_product_details_valid_returns_200():
    db = SessionLocal()
    category = Category(name="Test Details Category")
    db.add(category)
    db.commit()
    db.refresh(category)

    product = Product(
        name="Rose Bouquet",
        description="Detailed description for rose bouquet",
        price=120.0,
        stock=8,
        image_url="https://example.com/rose.jpg",
        is_featured=False,
        season=ProductSeason.SPRING,
        product_type=ProductType.BOUQUET,
        category_id=category.id,
    )
    db.add(product)
    db.commit()
    db.refresh(product)
    product_id = product.id

    try:
        response = client.get(f"/api/products/{product_id}")

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == product_id
        assert data["name"] == "Rose Bouquet"
        assert data["description"] == "Detailed description for rose bouquet"
        assert data["price"] == 120.0
        assert data["stock"] == 8
        assert data["season"] == "spring"
        assert data["product_type"] == "bouquet"
        assert data["category"]["id"] == category.id
        assert data["colors"] == []
    finally:
        db.delete(product)
        db.delete(category)
        db.commit()
        db.close()


def test_get_product_details_invalid_returns_404():
    response = client.get("/api/products/999999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Product not found"
