from fastapi import HTTPException
from sqlalchemy.orm import Session, joinedload

from app.models.category import Category
from app.models.color import Color
from app.models.product import Product, ProductSeason, ProductType


def _get_colors_by_ids(color_ids: list[int], db: Session) -> list[Color]:
    if not color_ids:
        return []

    unique_color_ids = sorted(set(color_ids))
    colors = db.query(Color).filter(Color.id.in_(unique_color_ids)).all()
    found_ids = {color.id for color in colors}
    missing_ids = [
        color_id for color_id in unique_color_ids if color_id not in found_ids
    ]

    if missing_ids:
        raise HTTPException(
            status_code=404,
            detail=f"Color not found: {missing_ids}",
        )

    return colors


def get_filtered_products(
    db: Session,
    search: str | None = None,
    category: str | None = None,
    product_type: ProductType | None = None,
    min_price: float | None = None,
    max_price: float | None = None,
    color_id: int | None = None,
) -> list[Product]:
    query = db.query(Product).options(
        joinedload(Product.category),
        joinedload(Product.colors),
    )

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

    if product_type is not None:
        query = query.filter(Product.product_type == product_type)

    if color_id is not None:
        color = db.query(Color).filter(Color.id == color_id).first()
        if not color:
            raise HTTPException(status_code=400, detail="Color not found")
        query = query.filter(Product.colors.any(Color.id == color_id))

    return query.order_by(Product.id.asc()).all()


def get_featured_products(db: Session) -> list[Product]:
    return (
        db.query(Product)
        .options(
            joinedload(Product.category),
            joinedload(Product.colors),
        )
        .filter(Product.is_featured.is_(True))
        .order_by(Product.id.asc())
        .all()
    )


def get_product_or_404(product_id: int, db: Session) -> Product:
    product = (
        db.query(Product)
        .options(
            joinedload(Product.category),
            joinedload(Product.colors),
        )
        .filter(Product.id == product_id)
        .first()
    )
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


def create_product(
    *,
    name: str,
    description: str,
    price: float,
    stock: int,
    image_url: str | None,
    is_featured: bool,
    season: ProductSeason,
    product_type: ProductType,
    color_ids: list[int],
    category_id: int,
    db: Session,
) -> Product:
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    colors = _get_colors_by_ids(color_ids=color_ids, db=db)

    product = Product(
        name=name,
        description=description,
        price=price,
        stock=stock,
        image_url=image_url,
        is_featured=is_featured,
        season=season,
        product_type=product_type,
        category_id=category_id,
        colors=colors,
    )
    db.add(product)
    db.commit()
    db.refresh(product)

    return (
        db.query(Product)
        .options(
            joinedload(Product.category),
            joinedload(Product.colors),
        )
        .filter(Product.id == product.id)
        .first()
    )


def update_product(
    *,
    product_id: int,
    name: str | None,
    description: str | None,
    price: float | None,
    stock: int | None,
    image_url: str | None,
    is_featured: bool | None,
    season: ProductSeason | None,
    product_type: ProductType | None,
    color_ids: list[int] | None,
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
    if description is not None:
        product.description = description
    if price is not None:
        product.price = price
    if stock is not None:
        product.stock = stock
    if image_url is not None:
        product.image_url = image_url
    if is_featured is not None:
        product.is_featured = is_featured
    if season is not None:
        product.season = season
    if product_type is not None:
        product.product_type = product_type
    if color_ids is not None:
        product.colors = _get_colors_by_ids(color_ids=color_ids, db=db)

    db.add(product)
    db.commit()
    db.refresh(product)

    return (
        db.query(Product)
        .options(
            joinedload(Product.category),
            joinedload(Product.colors),
        )
        .filter(Product.id == product.id)
        .first()
    )


def delete_product(product_id: int, db: Session) -> None:
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    db.delete(product)
    db.commit()
