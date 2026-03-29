from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_register_valid():
    response = client.post(
        "/api/auth/register",
        json={
            "name": "Ana",
            "email": "ana_test373@test.com",
            "password": "123456789",
            "confirm_password": "123456789",
        },
    )

    assert response.status_code == 201


def test_register_duplicate_email():
    email12 = "duplicate_test@test.com"

    client.post(
        "/api/auth/register",
        json={
            "name": "Ana",
            "email": email12,
            "password": "12345678",
            "confirm_password": "12345678",
        },
    )

    response = client.post(
        "/api/auth/register",
        json={
            "name": "Ana",
            "email": email12,
            "password": "12345678",
            "confirm_password": "12345678",
        },
    )

    assert response.status_code == 409
    assert response.json()["detail"] == "Email is already registered"


def test_register_short_password():
    response = client.post(
        "/api/auth/register",
        json={
            "name": "Ana",
            "email": "short_pass@test.com",
            "password": "123",
            "confirm_password": "123",
        },
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Password must be at least 8 characters long"


def test_register_password_mismatch():
    response = client.post(
        "/api/auth/register",
        json={
            "name": "Ana",
            "email": "mismatch@test.com",
            "password": "12345678",
            "confirm_password": "123456789",
        },
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Passwords do not match"


def test_register_admin_invalid_code():
    response = client.post(
        "/api/auth/register",
        json={
            "name": "Admin",
            "email": "admin_code@test.com",
            "password": "12345678",
            "confirm_password": "12345678",
            "role": "admin",
            "admin_code": "wrong-code",
        },
    )

    assert response.status_code == 403
    assert response.json()["detail"] == "Invalid admin code"