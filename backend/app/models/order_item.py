from sqlalchemy import JSON, Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.database.db import Base


class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(
        Integer,
        ForeignKey("orders.id", ondelete="CASCADE"),
        nullable=False,
    )
    product_id = Column(Integer, ForeignKey("products.id"), nullable=True)
    product_name = Column(String, nullable=True)
    color_id = Column(Integer, ForeignKey("colors.id"), nullable=True)
    color_name = Column(String, nullable=True)
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Float, nullable=False)
    line_total = Column(Float, nullable=False)
    composition = Column(JSON, nullable=True)

    order = relationship("Order", back_populates="items")
    product = relationship("Product")
    color = relationship("Color")
