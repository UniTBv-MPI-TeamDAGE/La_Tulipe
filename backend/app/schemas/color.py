from pydantic import BaseModel, Field


class ColorResponse(BaseModel):
    id: int
    name: str
    hex_code: str | None = None

    class Config:
        from_attributes = True


class ColorCreate(BaseModel):
    name: str = Field(min_length=1)
    hex_code: str | None = None


class ColorUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1)
    hex_code: str | None = None
