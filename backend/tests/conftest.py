import sys
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


@pytest.fixture(autouse=True)
def cleanup_test_users():
    """Cleanup test users from database after each test"""
    from app.database.db import SessionLocal
    from app.models.user import User

    yield

    db = SessionLocal()
    try:
        test_emails = [
            "ana_test373@test.com",
            "duplicate_test@test.com",
            "login_test@test.com",
            "wrong_pass_test@test.com",
        ]

        for email in test_emails:
            user = db.query(User).filter(User.email == email).first()
            if user:
                db.delete(user)

        db.commit()
    finally:
        db.close()
