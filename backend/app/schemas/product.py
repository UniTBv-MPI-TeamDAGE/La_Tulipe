from pydantic import BaseModel

from app.schemas.category import CategoryResponse


class ProductResponse(BaseModel):
    id: int
    name: str
    price: float
    stock: int
    image_url: str | None = None
    is_featured: bool
    category: CategoryResponse

    class Config:
        from_attributes = True
