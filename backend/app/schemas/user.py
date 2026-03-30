from pydantic import BaseModel, EmailStr


class UserMeResponse(BaseModel):
    name: str
    email: EmailStr
    phone: str | None = None


class UpdateMeRequest(BaseModel):
    name: str | None = None
    phone: str | None = None
