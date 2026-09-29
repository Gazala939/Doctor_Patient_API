import pytest
from fastapi.testclient import TestClient

from index import app


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def admin_token(client):
    response = client.post(
        "/auth/register",
        json={
            "name": "Test Admin",
            "email": "testadmin@example.com",
            "password": "Admin@123",
            "role": "Admin"
        }
    )

    response = client.post(
        "/auth/login",
        json={
            "email": "testadmin@example.com",
            "password": "Admin@123"
        }
    )

    return response.json()["access_token"]


@pytest.fixture
def doctor_token(client):
    response = client.post(
        "/auth/register",
        json={
            "name": "Test Doctor",
            "email": "testdoctor@example.com",
            "password": "Doctor@123",
            "role": "Doctor"
        }
    )

    response = client.post(
        "/auth/login",
        json={
            "email": "testdoctor@example.com",
            "password": "Doctor@123"
        }
    )

    return response.json()["access_token"]