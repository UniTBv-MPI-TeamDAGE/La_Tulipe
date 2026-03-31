import bcrypt
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.security import create_access_token
from app.models.user import User
from app.schemas.auth import LoginRequest, RegisterRequest


def register_user(
    data: RegisterRequest,
    db: Session,
    admin_registration_code: str | None,
) -> dict[str, str]:
    if len(data.password) < 8:
        raise HTTPException(
            status_code=400,
            detail="Password must be at least 8 characters long",
        )

    if data.password != data.confirm_password:
        raise HTTPException(status_code=400, detail="Passwords do not match")

    if data.role == "admin":
        if not admin_registration_code:
            raise HTTPException(
                status_code=500,
                detail="Admin registration is not configured",
            )
        if data.admin_code != admin_registration_code:
            raise HTTPException(status_code=403, detail="Invalid admin code")

    existing_user = db.query(User).filter(User.email == data.email).first()
    if existing_user:
        raise HTTPException(status_code=409, detail="Email is already registered")

    hashed = bcrypt.hashpw(data.password.encode(), bcrypt.gensalt()).decode()

    user = User(
        name=data.name,
        email=data.email,
        password_hash=hashed,
        role=data.role,
        phone=data.phone,
    )

    db.add(user)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="Email is already registered",
        ) from None

    db.refresh(user)
    return {"message": "User created"}


def login_user(data: LoginRequest, db: Session) -> dict[str, str]:
    user = db.query(User).filter(User.email == data.email).first()

    if not user or not bcrypt.checkpw(
        data.password.encode(),
        user.password_hash.encode(),
    ):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    token = create_access_token(user)
    return {
        "access_token": token,
        "token_type": "bearer",
        "name": user.name,
        "role": user.role,
    }


def logout_user() -> dict[str, str]:
    return {"message": "Logout successful"}
