from pydantic import BaseModel, Field

from app.models.product import ProductSeason, ProductType
from app.schemas.category import CategoryResponse
from app.schemas.color import ColorResponse


class ProductColorStockCreate(BaseModel):
    color_id: int
    stock: int = Field(ge=0)


class ProductColorStockResponse(BaseModel):
    color: ColorResponse
    stock: int

    class Config:
        from_attributes = True


class ProductResponse(BaseModel):
    id: int
    name: str
    description: str
    price: float
    stock: int
    image_url: str | None = None
    is_featured: bool
    season: ProductSeason
    product_type: ProductType
    category: CategoryResponse
    colors: list[ColorResponse]
    color_stocks: list[ProductColorStockResponse] = Field(default_factory=list)

    class Config:
        from_attributes = True


class ProductCreate(BaseModel):
    name: str
    description: str = ""
    price: float = Field(ge=0)
    stock: int = Field(ge=0)
    image_url: str | None = None
    is_featured: bool = False
    season: ProductSeason = ProductSeason.ALL_SEASON
    product_type: ProductType = ProductType.INDIVIDUAL
    color_stocks: list[ProductColorStockCreate] = Field(default_factory=list)
    category_id: int


class ProductUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    price: float | None = Field(default=None, ge=0)
    stock: int | None = Field(default=None, ge=0)
    image_url: str | None = None
    is_featured: bool | None = None
    season: ProductSeason | None = None
    product_type: ProductType | None = None
    color_stocks: list[ProductColorStockCreate] | None = None
    category_id: int | None = None


class ProductStockUpdate(BaseModel):
    stock: int
