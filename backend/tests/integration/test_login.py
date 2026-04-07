from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_login_valid():
    email = "login_test@test.com"
    password = "12345678"
    
    client.post(
        "/api/auth/register",
        json={
            "name": "Login User",
            "email": email,
            "password": password,
            "confirm_password": password,
        },
    )

    response = client.post(
        "/api/auth/login",
        json={
            "email": email,
            "password": password,
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert data["name"] == "Login User"
    assert data["role"] == "customer"


def test_login_invalid_password():
    email = "wrong_pass_test@test.com"
    password = "12345678"
    
    client.post(
        "/api/auth/register",
        json={
            "name": "Wrong Pass User",
            "email": email,
            "password": password,
            "confirm_password": password,
        },
    )

    response = client.post(
        "/api/auth/login",
        json={
            "email": email,
            "password": "wrongpassword",
        },
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid email or password"
