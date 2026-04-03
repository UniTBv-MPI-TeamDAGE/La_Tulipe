from enum import Enum

from sqlalchemy import (
    Boolean,
    Column,
    Float,
    ForeignKey,
    Integer,
    String,
    UniqueConstraint,
)
from sqlalchemy import (
    Enum as SqlEnum,
)
from sqlalchemy.orm import relationship

from app.database.db import Base


class ProductType(str, Enum):
    INDIVIDUAL = "individual"
    BOUQUET = "bouquet"


class ProductSeason(str, Enum):
    ALL_SEASON = "all_season"
    SPRING = "spring"
    SUMMER = "summer"
    AUTUMN = "autumn"
    WINTER = "winter"


class ProductColorStock(Base):
    __tablename__ = "product_color_stocks"
    __table_args__ = (
        UniqueConstraint(
            "product_id",
            "color_id",
            name="uq_product_color_stocks_product_color",
        ),
    )

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(
        Integer,
        ForeignKey("products.id", ondelete="CASCADE"),
        nullable=False,
    )
    color_id = Column(Integer, ForeignKey("colors.id"), nullable=False)
    stock = Column(Integer, default=0, nullable=False)

    product = relationship("Product", back_populates="color_stocks")
    color = relationship("Color", back_populates="product_stocks")


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False, default="")
    price = Column(Float, nullable=False)
    stock = Column(Integer, default=0, nullable=False)
    image_url = Column(String, nullable=True)
    is_featured = Column(Boolean, default=False, nullable=False)
    season = Column(
        SqlEnum(ProductSeason, name="product_season_enum"),
        nullable=False,
        default=ProductSeason.ALL_SEASON,
    )
    product_type = Column(
        SqlEnum(ProductType, name="product_type_enum"),
        nullable=False,
        default=ProductType.INDIVIDUAL,
    )
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)

    category = relationship("Category", backref="products")
    color_stocks = relationship(
        "ProductColorStock",
        back_populates="product",
        cascade="all, delete-orphan",
    )
    colors = relationship(
        "Color",
        secondary="product_color_stocks",
        back_populates="products",
        overlaps="color_stocks,product_stocks,product,color",
    )
