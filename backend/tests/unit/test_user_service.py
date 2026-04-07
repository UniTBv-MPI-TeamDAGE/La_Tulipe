import pytest
from unittest.mock import MagicMock

from app.services.user_service import get_me, update_me
from app.models.user import User
from app.schemas.user import UpdateMeRequest


def test_get_me():
    user = User(name="Ana", email="ana@test.com", phone="0712345678")

    result = get_me(user)

    assert result["name"] == "Ana"
    assert result["email"] == "ana@test.com"
    assert result["phone"] == "0712345678"


def test_update_me_name():
    db = MagicMock()
    user = User(name="Old", email="ana@test.com", phone="0712")

    data = UpdateMeRequest(name="New", phone=None)

    result = update_me(data, db, user)

    assert result["name"] == "New"
    assert user.name == "New"
    db.commit.assert_called_once()


def test_update_me_phone():
    db = MagicMock()
    user = User(name="Ana", email="ana@test.com", phone="0712")

    data = UpdateMeRequest(name=None, phone="0722")

    result = update_me(data, db, user)

    assert result["phone"] == "0722"
    assert user.phone == "0722"
    db.commit.assert_called_once()


def test_update_me_both_fields():
    db = MagicMock()
    user = User(name="Old", email="ana@test.com", phone="0712")

    data = UpdateMeRequest(name="New", phone="0733")

    result = update_me(data, db, user)

    assert result["name"] == "New"
    assert result["phone"] == "0733"
    db.commit.assert_called_once()


def test_update_me_no_changes():
    db = MagicMock()
    user = User(name="Ana", email="ana@test.com", phone="0712")

    data = UpdateMeRequest(name=None, phone=None)

    result = update_me(data, db, user)

    assert result["name"] == "Ana"
    assert result["phone"] == "0712"

    db.commit.assert_called_once()