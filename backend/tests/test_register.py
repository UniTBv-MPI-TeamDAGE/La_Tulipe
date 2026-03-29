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