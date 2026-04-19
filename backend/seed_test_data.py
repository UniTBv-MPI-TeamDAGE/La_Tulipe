import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.database.db import SessionLocal
from app.models.product import Product, ProductType, ProductSeason, ProductColorStock
from app.models.category import Category
from app.models.color import Color


def seed():
    db = SessionLocal()
    try:
        if db.query(Product).count() > 0:
            return

        category = Category(name="Flowers")
        db.add(category)
        db.flush()

        color = db.query(Color).first()

        products = [
            Product(name="Rose", description="Beautiful red rose", price=10.0, stock=100, is_featured=True, season=ProductSeason.ALL_SEASON, product_type=ProductType.INDIVIDUAL, category_id=category.id, image_url="https://images.pexels.com/photos/56866/garden-rose-red-pink-56866.jpeg"),
            Product(name="Tulip", description="Fresh tulip", price=8.0, stock=100, is_featured=False, season=ProductSeason.ALL_SEASON, product_type=ProductType.INDIVIDUAL, category_id=category.id, image_url="https://images.pexels.com/photos/56866/garden-rose-red-pink-56866.jpeg"),
            Product(name="Sunflower", description="Bright sunflower", price=6.0, stock=100, is_featured=False, season=ProductSeason.ALL_SEASON, product_type=ProductType.INDIVIDUAL, category_id=category.id, image_url="https://images.pexels.com/photos/56866/garden-rose-red-pink-56866.jpeg"),
        ]
        for p in products:
            db.add(p)
        db.flush()

        if color:
            for p in products:
                db.add(ProductColorStock(product_id=p.id, color_id=color.id, stock=100))

        db.commit()
        print("Seeded test data successfully.")
    finally:
        db.close()


if __name__ == "__main__":
    seed()