from pydantic import BaseModel, EmailStr

class RegisterRequest(BaseModel):
    nume: str
    email: EmailStr
    password: str
    confirm_password: str
    telefon: str| None= None
