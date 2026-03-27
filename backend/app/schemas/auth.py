from typing import Literal

from pydantic import BaseModel, EmailStr


class RegisterRequest(BaseModel):
    name: str
    email: EmailStr
    password: str
    confirm_password: str
    phone: str | None = None
    role: Literal["customer", "admin"] = "customer"
    admin_code: str | None = None


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    name: str
    role: str


class UserMeResponse(BaseModel):
    name: str
    email: EmailStr
    phone: str | None = None


class UpdateMeRequest(BaseModel):
    name: str | None = None
    phone: str | None = None
