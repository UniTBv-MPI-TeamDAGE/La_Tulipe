import os

import bcrypt

from app.database.db import SessionLocal
from app.models.user import User

DEFAULT_ADMIN_EMAIL = os.getenv("ADMIN_DEFAULT_EMAIL", "admin@latulipe.ro")
DEFAULT_ADMIN_NAME = os.getenv("ADMIN_DEFAULT_NAME", "Admin La Tulipe")
DEFAULT_ADMIN_PASSWORD = os.getenv("ADMIN_DEFAULT_PASSWORD", "default123")


def ensure_default_admin() -> None:
    db = SessionLocal()
    try:
        existing_admin = (
            db.query(User).filter(User.email == DEFAULT_ADMIN_EMAIL).first()
        )
        if existing_admin:
            return

        hashed = bcrypt.hashpw(
            DEFAULT_ADMIN_PASSWORD.encode(), bcrypt.gensalt()
        ).decode()

        admin = User(
            name=DEFAULT_ADMIN_NAME,
            email=DEFAULT_ADMIN_EMAIL,
            password_hash=hashed,
            role="admin",
            phone="0723658900",
        )
        db.add(admin)
        db.commit()
    finally:
        db.close()
