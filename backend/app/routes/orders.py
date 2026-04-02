from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.db import get_db
from app.middleware.auth import get_current_user
from app.models.user import User
from app.schemas.order import OrderCreate, OrderResponse
from app.services import order_service

router = APIRouter(prefix="/api/orders", tags=["orders"])


@router.post("", response_model=OrderResponse, status_code=201)
def create_order(
    data: OrderCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return order_service.create_order(data=data, current_user=current_user, db=db)


@router.get("/my-orders", response_model=list[OrderResponse])
def get_my_orders(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return order_service.get_my_orders(current_user=current_user, db=db)


@router.get("/{order_id}", response_model=OrderResponse)
def get_my_order_by_id(
    order_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return order_service.get_my_order_or_404(
        order_id=order_id,
        current_user=current_user,
        db=db,
    )
