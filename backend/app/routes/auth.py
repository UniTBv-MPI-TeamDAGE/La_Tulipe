import bcrypt
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.security import create_access_token
from app.database.db import get_db
from app.models.user import User
from app.schemas.auth import LoginRequest, LoginResponse, RegisterRequest

router = APIRouter()
ADMIN_REGISTRATION_CODE = "adminLT#2026"


@router.post("/api/auth/register", status_code=201)
def register(data: RegisterRequest, db: Session = Depends(get_db)):
    if len(data.password) < 8:
        raise HTTPException(
            status_code=400,
            detail="Parola trebuie sa aiba cel putin 8 caractere"
        )

    if data.password != data.confirm_password:
        raise HTTPException(
            status_code=400,
            detail="Parolele nu se potrivesc"
        )

    if data.role == "admin" and data.admin_code != ADMIN_REGISTRATION_CODE:
        raise HTTPException(status_code=403, detail="Cod admin invalid")

    existing_user = db.query(User).filter(User.email == data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=409,
            detail="Email-ul este deja folosit"
        )

    hashed = bcrypt.hashpw(
        data.password.encode(),
        bcrypt.gensalt()
    ).decode()

    user = User(
        nume=data.nume,
        email=data.email,
        password_hash=hashed,
        role=data.role,
        telefon=data.telefon
    )

    db.add(user)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="Email-ul este deja folosit"
        ) from None

    db.refresh(user)

    return {"message": "Utilizator creat"}


@router.post("/api/auth/login", response_model=LoginResponse)
def login(data: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == data.email).first()

    if not user or not bcrypt.checkpw(
        data.password.encode(), user.password_hash.encode()
    ):
        raise HTTPException(status_code=401, detail="Email sau parola incorecta")

    token = create_access_token(user)
    return {
        "access_token": token,
        "token_type": "bearer",
        "nume": user.nume,
        "role": user.role,
    }


@router.post("/api/auth/logout", status_code=200)
def logout():
    return {"message": "Logout realizat"}