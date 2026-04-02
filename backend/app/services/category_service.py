from fastapi import HTTPException
from sqlalchemy.orm import Session, joinedload

from app.models.category import Category
from app.models.product import Product


def get_categories(db: Session) -> list[Category]:
    return db.query(Category).order_by(Category.name.asc()).all()


def get_category_or_404(category_id: int, db: Session) -> Category:
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category


def get_products_by_category(category_id: int, db: Session) -> list[Product]:
    get_category_or_404(category_id=category_id, db=db)

    return (
        db.query(Product)
        .options(joinedload(Product.category))
        .filter(Product.category_id == category_id)
        .order_by(Product.id.asc())
        .all()
    )


def create_category(name: str, db: Session) -> Category:
    existing = db.query(Category).filter(Category.name == name).first()
    if existing:
        raise HTTPException(status_code=409, detail="Category already exists")

    category = Category(name=name)
    db.add(category)
    db.commit()
    db.refresh(category)
    return category


def update_category(category_id: int, name: str | None, db: Session) -> Category:
    category = get_category_or_404(category_id=category_id, db=db)

    if name is not None:
        category.name = name

    db.add(category)
    db.commit()
    db.refresh(category)
    return category


def delete_category(category_id: int, db: Session) -> None:
    category = get_category_or_404(category_id=category_id, db=db)
    db.delete(category)
    db.commit()
