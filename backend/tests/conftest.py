import pytest

from app.database.db import SessionLocal
from app.models.user import User


@pytest.fixture(autouse=True)
def cleanup_test_users():
    """Cleanup test users from database after each test"""
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
