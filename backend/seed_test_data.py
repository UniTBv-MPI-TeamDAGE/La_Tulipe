import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.database.db import SessionLocal
from app.models.category import Category
from app.models.color import Color 
from app.models.order import Order  
from app.models.order_item import OrderItem 
from app.models.product import Product, ProductSeason, ProductType
from app.models.user import User  


def seed() -> None:
    db = SessionLocal()
    try:
        if db.query(Product).count() > 0:
            return

        category = Category(name="Flowers")
        db.add(category)
        db.flush()

        img = "https://images.pexels.com/photos/56866/garden-rose-red-pink-56866.jpeg"

        products = [
            Product(
                name="Rose",
                description="Beautiful red rose",
                price=10.0,
                stock=100,
                is_featured=True,
                season=ProductSeason.ALL_SEASON,
                product_type=ProductType.INDIVIDUAL,
                category_id=category.id,
                image_url=img,
            ),
            Product(
                name="Tulip",
                description="Fresh tulip",
                price=8.0,
                stock=100,
                is_featured=False,
                season=ProductSeason.ALL_SEASON,
                product_type=ProductType.INDIVIDUAL,
                category_id=category.id,
                image_url=img,
            ),
            Product(
                name="Sunflower",
                description="Bright sunflower",
                price=6.0,
                stock=100,
                is_featured=False,
                season=ProductSeason.ALL_SEASON,
                product_type=ProductType.INDIVIDUAL,
                category_id=category.id,
                image_url=img,
            ),
        ]
        for p in products:
            db.add(p)

        db.commit()
        print("Seeded test data successfully.")
    finally:
        db.close()


if __name__ == "__main__":
    seed()