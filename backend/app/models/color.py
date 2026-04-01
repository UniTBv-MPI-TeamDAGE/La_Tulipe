from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.database.db import Base


class Color(Base):
    __tablename__ = "colors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    hex_code = Column(String, nullable=True)

    products = relationship(
        "Product",
        secondary="product_colors",
        back_populates="colors",
    )
