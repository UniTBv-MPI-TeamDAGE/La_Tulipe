from fastapi import HTTPException
from sqlalchemy.orm import Session, joinedload

from app.models.category import Category
from app.models.color import Color
from app.models.product import Product, ProductColorStock, ProductSeason, ProductType


def _get_colors_by_id_list(color_id_list: list[int], db: Session) -> list[Color]:
    if not color_id_list:
        return []

    unique_color_id_list = sorted(set(color_id_list))
    colors = db.query(Color).filter(Color.id.in_(unique_color_id_list)).all()
    found_ids = {color.id for color in colors}
    missing_ids = [
        color_id for color_id in unique_color_id_list if color_id not in found_ids
    ]

    if missing_ids:
        raise HTTPException(
            status_code=404,
            detail=f"Color not found: {missing_ids}",
        )

    return colors


def _resolve_color_stock_pairs(
    *,
    color_stocks: list[tuple[int, int]] | None,
) -> list[tuple[int, int]]:
    if color_stocks:
        normalized_pairs: list[tuple[int, int]] = []
        seen_color_ids: set[int] = set()

        for color_id, stock in color_stocks:
            if color_id in seen_color_ids:
                raise HTTPException(
                    status_code=400,
                    detail=f"Duplicate color_id in color_stocks: {color_id}",
                )
            if stock < 0:
                raise HTTPException(
                    status_code=400,
                    detail=f"Invalid stock for color_id {color_id}: {stock}",
                )
            seen_color_ids.add(color_id)
            normalized_pairs.append((color_id, stock))

        return normalized_pairs

    return []


def _validate_color_stock_total(
    *,
    total_stock: int,
    color_stock_pairs: list[tuple[int, int]],
) -> None:
    if not color_stock_pairs:
        return

    total_color_stock = sum(stock for _, stock in color_stock_pairs)
    if total_color_stock > total_stock:
        raise HTTPException(
            status_code=400,
            detail=(
                "Sum of color-specific stocks cannot exceed product total stock "
                f"({total_color_stock} > {total_stock})"
            ),
        )


def _set_product_color_stocks(
    *,
    product: Product,
    color_stock_pairs: list[tuple[int, int]],
    db: Session,
) -> None:
    if not color_stock_pairs:
        product.color_stocks = []
        return

    color_id_list = [color_id for color_id, _ in color_stock_pairs]
    _get_colors_by_id_list(color_id_list=color_id_list, db=db)

    product.color_stocks = [
        ProductColorStock(color_id=color_id, stock=stock)
        for color_id, stock in color_stock_pairs
    ]


def _merge_product_color_stocks(
    *,
    product: Product,
    incoming_color_stock_pairs: list[tuple[int, int]],
    total_stock: int,
    db: Session,
) -> None:
    if not incoming_color_stock_pairs:
        return

    incoming_color_ids = [color_id for color_id, _ in incoming_color_stock_pairs]
    _get_colors_by_id_list(color_id_list=incoming_color_ids, db=db)

    existing_color_stocks_by_color_id = {
        color_stock.color_id: color_stock for color_stock in product.color_stocks
    }

    for color_id, stock in incoming_color_stock_pairs:
        existing_color_stock = existing_color_stocks_by_color_id.get(color_id)
        if existing_color_stock is not None:
            existing_color_stock.stock = stock
            continue

        product.color_stocks.append(
            ProductColorStock(
                color_id=color_id,
                stock=stock,
            )
        )

    merged_color_stock_pairs = [
        (color_stock.color_id, color_stock.stock)
        for color_stock in product.color_stocks
    ]
    _validate_color_stock_total(
        total_stock=total_stock,
        color_stock_pairs=merged_color_stock_pairs,
    )


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
        joinedload(Product.color_stocks).joinedload(ProductColorStock.color),
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
        query = query.filter(
            Product.color_stocks.any(ProductColorStock.color_id == color_id)
        )

    return query.order_by(Product.id.asc()).all()


def get_featured_products(db: Session) -> list[Product]:
    return (
        db.query(Product)
        .options(
            joinedload(Product.category),
            joinedload(Product.colors),
            joinedload(Product.color_stocks).joinedload(ProductColorStock.color),
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
            joinedload(Product.color_stocks).joinedload(ProductColorStock.color),
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
    color_stocks: list[tuple[int, int]],
    category_id: int,
    db: Session,
) -> Product:
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    resolved_color_stocks = _resolve_color_stock_pairs(
        color_stocks=color_stocks,
    )
    if resolved_color_stocks:
        _validate_color_stock_total(
            total_stock=stock,
            color_stock_pairs=resolved_color_stocks,
        )

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
    )
    _set_product_color_stocks(
        product=product,
        color_stock_pairs=resolved_color_stocks,
        db=db,
    )
    db.add(product)
    db.commit()
    db.refresh(product)

    return (
        db.query(Product)
        .options(
            joinedload(Product.category),
            joinedload(Product.colors),
            joinedload(Product.color_stocks).joinedload(ProductColorStock.color),
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
    color_stocks: list[tuple[int, int]] | None,
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
    if image_url is not None:
        product.image_url = image_url
    if is_featured is not None:
        product.is_featured = is_featured
    if season is not None:
        product.season = season
    if product_type is not None:
        product.product_type = product_type

    target_stock = stock if stock is not None else product.stock

    if color_stocks is not None:
        resolved_color_stocks = _resolve_color_stock_pairs(
            color_stocks=color_stocks,
        )
        if resolved_color_stocks:
            _merge_product_color_stocks(
                product=product,
                incoming_color_stock_pairs=resolved_color_stocks,
                total_stock=target_stock,
                db=db,
            )
        else:
            product.color_stocks = []
    elif stock is not None and product.color_stocks:
        existing_color_stocks = [
            (item.color_id, item.stock)
            for item in product.color_stocks
        ]
        if existing_color_stocks:
            _validate_color_stock_total(
                total_stock=stock,
                color_stock_pairs=existing_color_stocks,
            )

    if stock is not None:
        product.stock = stock

    db.add(product)
    db.commit()
    db.refresh(product)

    return (
        db.query(Product)
        .options(
            joinedload(Product.category),
            joinedload(Product.colors),
            joinedload(Product.color_stocks).joinedload(ProductColorStock.color),
        )
        .filter(Product.id == product.id)
        .first()
    )


def update_product_stock(
    *,
    product_id: int,
    stock: int,
    db: Session,
) -> Product:
    if stock < 0:
        raise HTTPException(status_code=400, detail="Stock cannot be negative")

    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    if product.color_stocks:
        existing_color_stocks = [
            (item.color_id, item.stock)
            for item in product.color_stocks
        ]
        _validate_color_stock_total(
            total_stock=stock,
            color_stock_pairs=existing_color_stocks,
        )

    product.stock = stock

    db.add(product)
    db.commit()
    db.refresh(product)

    return (
        db.query(Product)
        .options(
            joinedload(Product.category),
            joinedload(Product.colors),
            joinedload(Product.color_stocks).joinedload(ProductColorStock.color),
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
