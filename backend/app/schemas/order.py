from datetime import datetime

from pydantic import BaseModel, EmailStr, Field

from app.models.order import OrderStatus
from app.schemas.order_item import OrderItemCreate, OrderItemResponse


class OrderCreate(BaseModel):
    customer_name: str = Field(min_length=1)
    customer_email: EmailStr
    customer_phone: str = Field(min_length=1)
    delivery_address: str = Field(min_length=1)
    card_message: str | None = None
    items: list[OrderItemCreate] = Field(min_length=1)


class OrderResponse(BaseModel):
    id: int
    order_number: str
    customer_name: str
    customer_email: EmailStr
    customer_phone: str
    delivery_address: str
    card_message: str | None = None
    total_price: float
    status: OrderStatus
    created_at: datetime
    items: list[OrderItemResponse]

    class Config:
        from_attributes = True


class OrderStatusUpdate(BaseModel):
    status: OrderStatus
