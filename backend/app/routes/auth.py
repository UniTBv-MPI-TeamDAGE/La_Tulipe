from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
import bcrypt

from app.database.db import SessionLocal
from app.models.user import User
from app.schemas.auth import RegisterRequest

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


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
        role="customer",
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