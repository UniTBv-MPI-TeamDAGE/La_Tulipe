import os

import bcrypt
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.security import create_access_token
from app.database.db import get_db
from app.models.user import User
from app.schemas.auth import LoginRequest, LoginResponse, RegisterRequest

router = APIRouter()
ADMIN_REGISTRATION_CODE = os.getenv("ADMIN_REGISTRATION_CODE")


@router.post("/api/auth/register", status_code=201)
def register(data: RegisterRequest, db: Session = Depends(get_db)):
    if len(data.password) < 8:
        raise HTTPException(
            status_code=400,
            detail="Password must be at least 8 characters long"
        )

    if data.password != data.confirm_password:
        raise HTTPException(
            status_code=400,
            detail="Passwords do not match"
        )

    if data.role == "admin":
        if not ADMIN_REGISTRATION_CODE:
            raise HTTPException(
                status_code=500,
                detail="Admin registration is not configured",
            )
        if data.admin_code != ADMIN_REGISTRATION_CODE:
            raise HTTPException(status_code=403, detail="Invalid admin code")

    existing_user = db.query(User).filter(User.email == data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=409,
            detail="Email is already registered"
        )

    hashed = bcrypt.hashpw(
        data.password.encode(),
        bcrypt.gensalt()
    ).decode()

    user = User(
        name=data.name,
        email=data.email,
        password_hash=hashed,
        role=data.role,
        phone=data.phone
    )

    db.add(user)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="Email is already registered"
        ) from None

    db.refresh(user)

    return {"message": "User created"}


@router.post("/api/auth/login", response_model=LoginResponse)
def login(data: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.email).first()

    if not user or not bcrypt.checkpw(
        data.password.encode(), user.password_hash.encode()
    ):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    token = create_access_token(user)
    return {
        "access_token": token,
        "token_type": "bearer",
        "name": user.name,
        "role": user.role,
    }


@router.post("/api/auth/logout", status_code=200)
def logout():
    return {"message": "Logout successful"}