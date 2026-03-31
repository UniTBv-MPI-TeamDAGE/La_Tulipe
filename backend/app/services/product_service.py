from fastapi import HTTPException
from sqlalchemy.orm import Session, joinedload

from app.models.category import Category
from app.models.product import Product


def get_filtered_products(
    db: Session,
    search: str | None = None,
    category: str | None = None,
    min_price: float | None = None,
    max_price: float | None = None,
) -> list[Product]:
    query = db.query(Product).options(joinedload(Product.category))

    if search:
        search_value = search.strip()
        if search_value:
            query = query.filter(Product.name.ilike(f"%{search_value}%"))

    if category:
        category_value = category.strip()
        if category_value:
            if category_value.isdigit():
                query = query.filter(Product.category_id == int(category_value))
            else:
                query = query.join(Product.category).filter(
                    Category.name.ilike(category_value)
                )

    if min_price is not None:
        query = query.filter(Product.price >= min_price)

    if max_price is not None:
        query = query.filter(Product.price <= max_price)

    return query.order_by(Product.id.asc()).all()


def get_featured_products(db: Session) -> list[Product]:
    return (
        db.query(Product)
        .options(joinedload(Product.category))
        .filter(Product.is_featured.is_(True))
        .order_by(Product.id.asc())
        .all()
    )


def get_product_or_404(product_id: int, db: Session) -> Product:
    product = (
        db.query(Product)
        .options(joinedload(Product.category))
        .filter(Product.id == product_id)
        .first()
    )
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


def create_product(
    *,
    name: str,
    price: float,
    stock: int,
    image_url: str | None,
    is_featured: bool,
    category_id: int,
    db: Session,
) -> Product:
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    product = Product(
        name=name,
        price=price,
        stock=stock,
        image_url=image_url,
        is_featured=is_featured,
        category_id=category_id,
    )
    db.add(product)
    db.commit()
    db.refresh(product)

    return (
        db.query(Product)
        .options(joinedload(Product.category))
        .filter(Product.id == product.id)
        .first()
    )


def update_product(
    *,
    product_id: int,
    name: str | None,
    price: float | None,
    stock: int | None,
    image_url: str | None,
    is_featured: bool | None,
    category_id: int | None,
    db: Session,
) -> Product:
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    if category_id is not None:
        category = db.query(Category).filter(Category.id == category_id).first()
        if not category:
            raise HTTPException(status_code=404, detail="Category not found")
        product.category_id = category_id

    if name is not None:
        product.name = name
    if price is not None:
        product.price = price
    if stock is not None:
        product.stock = stock
    if image_url is not None:
        product.image_url = image_url
    if is_featured is not None:
        product.is_featured = is_featured

    db.add(product)
    db.commit()
    db.refresh(product)

    return (
        db.query(Product)
        .options(joinedload(Product.category))
        .filter(Product.id == product.id)
        .first()
    )


def delete_product(product_id: int, db: Session) -> None:
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    db.delete(product)
    db.commit()
