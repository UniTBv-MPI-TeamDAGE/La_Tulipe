from pydantic import BaseModel, Field

from app.models.product import ProductType
from app.schemas.category import CategoryResponse


class ProductResponse(BaseModel):
    id: int
    name: str
    price: float
    stock: int
    image_url: str | None = None
    is_featured: bool
    product_type: ProductType
    category: CategoryResponse

    class Config:
        from_attributes = True


class ProductCreate(BaseModel):
    name: str
    price: float = Field(ge=0)
    stock: int = Field(ge=0)
    image_url: str | None = None
    is_featured: bool = False
    product_type: ProductType = ProductType.INDIVIDUAL
    category_id: int


class ProductUpdate(BaseModel):
    name: str | None = None
    price: float | None = Field(default=None, ge=0)
    stock: int | None = Field(default=None, ge=0)
    image_url: str | None = None
    is_featured: bool | None = None
    product_type: ProductType | None = None
    category_id: int | None = None
