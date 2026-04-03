from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.database.db import Base


class Color(Base):
    __tablename__ = "colors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    hex_code = Column(String, nullable=True)

    product_stocks = relationship(
        "ProductColorStock",
        back_populates="color",
        cascade="all, delete-orphan",
    )
    products = relationship(
        "Product",
        secondary="product_color_stocks",
        back_populates="colors",
        overlaps="product_stocks,color_stocks,product,color",
    )
