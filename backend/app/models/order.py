from enum import Enum

from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String, func
from sqlalchemy import Enum as SqlEnum
from sqlalchemy.orm import relationship

from app.database.db import Base


class OrderStatus(str, Enum):
    PENDING= "pending"
    CONFIRMED= "confirmed"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    order_number = Column(String, unique=True, nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    customer_name = Column(String, nullable=False)
    customer_email = Column(String, nullable=False)
    customer_phone = Column(String, nullable=False)
    delivery_address = Column(String, nullable=False)
    card_message = Column(String, nullable=True)
    total_price = Column(Float, nullable=False, default=0)
    status = Column(
        SqlEnum(OrderStatus, name="order_status_enum"),
        nullable=False,
        default=OrderStatus.PENDING,
    )
    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    user = relationship("User", backref="orders")
    items = relationship(
        "OrderItem",
        back_populates="order",
        cascade="all, delete-orphan",
    )
