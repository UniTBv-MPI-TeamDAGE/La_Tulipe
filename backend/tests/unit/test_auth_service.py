from unittest.mock import MagicMock

import pytest
from fastapi import HTTPException

from app.models.user import User
from app.schemas.auth import LoginRequest, RegisterRequest
from app.services.auth_service import (
    login_user,
    logout_user,
    register_user,
)


def make_register_data(**overrides):
    base = dict(
        name="Ana",
        email="ana@test.com",
        password="12345678",
        confirm_password="12345678",
        role="customer",
        phone=None,
        admin_code=None,
    )
    base.update(overrides)
    return RegisterRequest(**base)


def test_register_password_too_short():
    db = MagicMock()
    data = make_register_data(password="123", confirm_password="123")

    with pytest.raises(HTTPException) as e:
        register_user(data, db, None)

    assert e.value.status_code == 400


def test_register_password_mismatch():
    db = MagicMock()
    data = make_register_data(confirm_password="wrong")

    with pytest.raises(HTTPException) as e:
        register_user(data, db, None)

    assert e.value.status_code == 400


def test_register_admin_invalid_code():
    db = MagicMock()
    data = make_register_data(role="admin", admin_code="bad")

    with pytest.raises(HTTPException) as e:
        register_user(data, db, "correct-code")

    assert e.value.status_code == 403


def test_register_existing_email():
    db = MagicMock()
    db.query().filter().first.return_value = User()

    data = make_register_data(email="exists@test.com")

    with pytest.raises(HTTPException) as e:
        register_user(data, db, None)

    assert e.value.status_code == 409


def test_login_user_not_found():
    db = MagicMock()
    db.query().filter().first.return_value = None

    data = LoginRequest(email="x@test.com", password="12345678")

    with pytest.raises(HTTPException) as e:
        login_user(data, db)

    assert e.value.status_code == 401


def test_login_wrong_password():
    db = MagicMock()
    
    import bcrypt
    correct_password = "12345678"
    hashed = bcrypt.hashpw(correct_password.encode(), bcrypt.gensalt()).decode()

    user = User(
        name="Ana",
        email="ana@test.com",
        password_hash=hashed,
        role="customer",
    )
    
    db.query().filter().first.return_value = user

    data = LoginRequest(email="ana@test.com", password="wrong")

    with pytest.raises(HTTPException):
        login_user(data, db)


def test_login_success(monkeypatch):
    db = MagicMock()

    import bcrypt
    password = "12345678"
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    user = User(
        name="Ana",
        email="ana@test.com",
        password_hash=hashed,
        role="customer",
    )
    db.query().filter().first.return_value = user

    monkeypatch.setattr(
        "app.services.auth_service.create_access_token",
        lambda u: "fake-token"
    )

    data = LoginRequest(email="ana@test.com", password=password)

    res = login_user(data, db)

    assert res["access_token"] == "fake-token"
    assert res["name"] == "Ana"
    assert res["role"] == "customer"

def test_logout():
    assert logout_user()["message"] == "Logout successful"