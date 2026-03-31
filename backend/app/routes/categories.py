from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.db import get_db
from app.middleware.auth import get_current_admin
from app.models.user import User
from app.schemas.category import (
    CategoryCreate,
    CategoryResponse,
    CategoryUpdate,
)
from app.schemas.product import ProductResponse
from app.services import category_service

router = APIRouter(prefix="/api/categories", tags=["categories"])


@router.get("", response_model=list[CategoryResponse])
def get_categories(db: Session = Depends(get_db)):
    return category_service.get_categories(db=db)


@router.get("/{category_id}", response_model=CategoryResponse)
def get_category(category_id: int, db: Session = Depends(get_db)):
    return category_service.get_category_or_404(category_id=category_id, db=db)


@router.get("/{category_id}/products", response_model=list[ProductResponse])
def get_products_by_category(category_id: int, db: Session = Depends(get_db)):
    return category_service.get_products_by_category(category_id=category_id, db=db)


@router.post("", response_model=CategoryResponse, status_code=201)
def create_category(
    data: CategoryCreate,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    return category_service.create_category(name=data.name, db=db)


@router.put("/{category_id}", response_model=CategoryResponse)
def update_category(
    category_id: int,
    data: CategoryUpdate,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    return category_service.update_category(
        category_id=category_id,
        name=data.name,
        db=db,
    )


@router.delete("/{category_id}", status_code=204)
def delete_category(
    category_id: int,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    category_service.delete_category(category_id=category_id, db=db)
