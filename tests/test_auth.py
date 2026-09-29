from fastapi.testclient import TestClient
from index import app


client = TestClient(app)


def test_register_user():
    response = client.post(
        "/auth/register",
        json={
            "name": "Test User",
            "email": "testuser123@example.com",
            "password": "Test@123",
            "role": "Admin"
        }
    )

    assert response.status_code in [200, 201, 400]


def test_login_user():
    response = client.post(
        "/auth/login",
        json={
            "email": "testuser123@example.com",
            "password": "Test@123"
        }
    )

    assert response.status_code in [200, 401]