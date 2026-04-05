from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.database.db import get_db
from app.middleware.auth import get_current_admin, get_current_user
from app.models.order import OrderStatus
from app.models.user import User
from app.schemas.order import OrderCreate, OrderResponse, OrderStatusUpdate
from app.services import order_service

router = APIRouter(prefix="/api/orders", tags=["orders"])
admin_router = APIRouter(prefix="/api/admin/orders", tags=["admin-orders"])


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


@admin_router.get("", response_model=list[OrderResponse])
def get_all_orders_for_admin(
    status: OrderStatus | None = Query(default=None),
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    return order_service.get_all_orders_for_admin(db=db, status=status)


@router.patch("/{order_id}/status", response_model=OrderResponse)
def update_order_status_for_admin(
    order_id: int,
    data: OrderStatusUpdate,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db),
):
    return order_service.update_order_status_for_admin(
        order_id=order_id,
        new_status=data.status,
        db=db,
    )
