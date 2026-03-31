import os

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.db import get_db
from app.schemas.auth import LoginRequest, LoginResponse, RegisterRequest
from app.services import auth_service

router = APIRouter()
ADMIN_REGISTRATION_CODE = os.getenv("ADMIN_REGISTRATION_CODE")


@router.post("/api/auth/register", status_code=201)
def register(data: RegisterRequest, db: Session = Depends(get_db)):
    return auth_service.register_user(
        data=data,
        db=db,
        admin_registration_code=ADMIN_REGISTRATION_CODE,
    )


@router.post("/api/auth/login", response_model=LoginResponse)
def login(data: LoginRequest, db: Session = Depends(get_db)):
    return auth_service.login_user(data=data, db=db)


@router.post("/api/auth/logout", status_code=200)
def logout():
    return auth_service.logout_user()