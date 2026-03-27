import os
from datetime import datetime, timedelta, timezone

import jwt

from app.models.user import User

SECRET_KEY = os.getenv("SECRET_KEY", "change-this-secret")
ALGORITHM = "HS256"


def get_expiry_seconds() -> int:
    raw_value = os.getenv("JWT_EXPIRY", "3600")
    try:
        parsed = int(raw_value)
    except ValueError:
        return 3600

    return parsed if parsed > 0 else 3600


def create_access_token(user: User) -> str:
    expiry = datetime.now(timezone.utc) + timedelta(seconds=get_expiry_seconds())
    payload = {
        "sub": str(user.id),
        "email": user.email,
        "nume": user.nume,
        "role": user.role,
        "exp": expiry,
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def decode_access_token(token: str) -> dict:
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
