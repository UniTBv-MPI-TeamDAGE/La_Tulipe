from pydantic import BaseModel, Field


class OrderItemCreate(BaseModel):
    product_id: int
    color_id: int | None = None
    quantity: int = Field(ge=1)


class OrderItemResponse(BaseModel):
    id: int
    product_id: int
    product_name: str
    color_id: int | None = None
    color_name: str | None = None
    quantity: int
    unit_price: float
    line_total: float

    class Config:
        from_attributes = True
