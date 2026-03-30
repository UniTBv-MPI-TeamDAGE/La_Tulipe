from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload

from app.database.db import get_db
from app.middleware.auth import get_current_admin
from app.models.category import Category
from app.models.product import Product
from app.models.user import User
from app.schemas.product import ProductCreate, ProductResponse, ProductUpdate

router = APIRouter(prefix="/api/products", tags=["products"])


@router.get("", response_model=list[ProductResponse])
def get_products(db: Session = Depends(get_db)):
    return (
        db.query(Product)
        .options(joinedload(Product.category))
        .order_by(Product.id.asc())
        .all()
    )


@router.get("/featured", response_model=list[ProductResponse])
def get_featured_products(db: Session = Depends(get_db)):
    return (
        db.query(Product)
        .options(joinedload(Product.category))
        .filter(Product.is_featured.is_(True))
        .order_by(Product.id.asc())
        .all()
    )


@router.get("/{product_id}", response_model=ProductResponse)
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = (
        db.query(Product)
        .options(joinedload(Product.category))
        .filter(Product.id == product_id)
        .first()
    )
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@router.post("", response_model=ProductResponse, status_code=201)
def create_product(
    data: ProductCreate,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    category = db.query(Category).filter(Category.id == data.category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    product = Product(
        name=data.name,
        price=data.price,
        stock=data.stock,
        image_url=data.image_url,
        is_featured=data.is_featured,
        category_id=data.category_id,
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


@router.put("/{product_id}", response_model=ProductResponse)
def update_product(
    product_id: int,
    data: ProductUpdate,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    if data.category_id is not None:
        category = db.query(Category).filter(Category.id == data.category_id).first()
        if not category:
            raise HTTPException(status_code=404, detail="Category not found")
        product.category_id = data.category_id

    if data.name is not None:
        product.name = data.name
    if data.price is not None:
        product.price = data.price
    if data.stock is not None:
        product.stock = data.stock
    if data.image_url is not None:
        product.image_url = data.image_url
    if data.is_featured is not None:
        product.is_featured = data.is_featured

    db.add(product)
    db.commit()
    db.refresh(product)

    return (
        db.query(Product)
        .options(joinedload(Product.category))
        .filter(Product.id == product.id)
        .first()
    )


@router.delete("/{product_id}", status_code=204)
def delete_product(
    product_id: int,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    db.delete(product)
    db.commit()
