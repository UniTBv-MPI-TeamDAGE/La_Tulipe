from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.database.db import get_db
from app.middleware.auth import get_current_admin
from app.models.product import ProductType
from app.models.user import User
from app.schemas.product import (
    ProductCreate,
    ProductResponse,
    ProductStockUpdate,
    ProductUpdate,
)
from app.services import product_service

router = APIRouter(prefix="/api/products", tags=["products"])


@router.get("", response_model=list[ProductResponse])
def get_products(
    search: str | None = Query(default=None, min_length=2),
    category: str | None = Query(default=None),
    product_type: ProductType | None = Query(default=None, alias="type"),
    color_id: int | None = Query(default=None, alias="color"),
    min_price: float | None = Query(default=None, ge=0),
    max_price: float | None = Query(default=None, ge=0),
    db: Session = Depends(get_db),
):
    if min_price is not None and max_price is not None and min_price > max_price:
        raise HTTPException(
            status_code=400,
            detail="min_price cannot be greater than max_price",
        )

    return product_service.get_filtered_products(
        db=db,
        search=search,
        category=category,
        product_type=product_type,
        min_price=min_price,
        max_price=max_price,
        color_id=color_id,
    )


@router.get("/featured", response_model=list[ProductResponse])
def get_featured_products(db: Session = Depends(get_db)):
    return product_service.get_featured_products(db=db)


@router.get("/{product_id}", response_model=ProductResponse)
def get_product(product_id: int, db: Session = Depends(get_db)):
    return product_service.get_product_or_404(product_id=product_id, db=db)


@router.post("", response_model=ProductResponse, status_code=201)
def create_product(
    data: ProductCreate,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    return product_service.create_product(
        name=data.name,
        description=data.description,
        price=data.price,
        stock=data.stock,
        image_url=data.image_url,
        is_featured=data.is_featured,
        season=data.season,
        product_type=data.product_type,
        color_stocks=[(item.color_id, item.stock) for item in data.color_stocks],
        category_id=data.category_id,
        db=db,
    )


@router.put("/{product_id}", response_model=ProductResponse)
def update_product(
    product_id: int,
    data: ProductUpdate,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    return product_service.update_product(
        product_id=product_id,
        name=data.name,
        description=data.description,
        price=data.price,
        stock=data.stock,
        image_url=data.image_url,
        is_featured=data.is_featured,
        season=data.season,
        product_type=data.product_type,
        color_stocks=(
            [(item.color_id, item.stock) for item in data.color_stocks]
            if data.color_stocks is not None
            else None
        ),
        category_id=data.category_id,
        db=db,
    )


@router.patch("/{product_id}/stock", response_model=ProductResponse)
def update_product_stock(
    product_id: int,
    data: ProductStockUpdate,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    return product_service.update_product_stock(
        product_id=product_id,
        stock=data.stock,
        db=db,
    )


@router.delete("/{product_id}", status_code=204)
def delete_product(
    product_id: int,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    product_service.delete_product(product_id=product_id, db=db)
