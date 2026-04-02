from enum import Enum

from sqlalchemy import (
    Boolean,
    Column,
    Float,
    ForeignKey,
    Integer,
    String,
    Table,
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


product_colors = Table(
    "product_colors",
    Base.metadata,
    Column("product_id", Integer, ForeignKey("products.id"), primary_key=True),
    Column("color_id", Integer, ForeignKey("colors.id"), primary_key=True),
)


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
    colors = relationship("Color", secondary=product_colors, back_populates="products")
