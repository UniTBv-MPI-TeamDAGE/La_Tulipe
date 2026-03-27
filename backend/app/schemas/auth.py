from typing import Literal

from pydantic import BaseModel, EmailStr


class RegisterRequest(BaseModel):
    nume: str
    email: EmailStr
    password: str
    confirm_password: str
    telefon: str | None = None
    role: Literal["customer", "admin"] = "customer"


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    nume: str
    role: str
