from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_register_valid():
    response = client.post(
        "/api/auth/register",
        json={
            "nume": "Ana",
            "email": "ana_test1@test.com",
            "password": "12345678",
            "confirm_password": "12345678",
        },
    )

    assert response.status_code == 201


def test_register_duplicate_email():
    email = "duplicate_test@test.com"

    client.post(
        "/api/auth/register",
        json={
            "nume": "Ana",
            "email": email,
            "password": "12345678",
            "confirm_password": "12345678",
        },
    )

    response = client.post(
        "/api/auth/register",
        json={
            "nume": "Ana",
            "email": email,
            "password": "12345678",
            "confirm_password": "12345678",
        },
    )

    assert response.status_code == 409