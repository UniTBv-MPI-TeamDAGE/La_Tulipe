from pydantic import BaseModel, Field


class CustomCompositionItem(BaseModel):
    product_id: int
    color_id: int | None = None
    quantity: int = Field(ge=1)


class OrderItemCreate(BaseModel):
    product_id: int | None = None
    color_id: int | None = None
    quantity: int = Field(ge=1)
    custom_composition: list[CustomCompositionItem] | None = None


class OrderItemResponse(BaseModel):
    id: int
    product_id: int | None
    product_name: str | None
    color_id: int | None = None
    color_name: str | None = None
    quantity: int
    unit_price: float
    line_total: float
    composition: str | None = None

    class Config:
        from_attributes = True
