from fastapi.testclient import TestClient

from index import app

from uuid import uuid4

client = TestClient(app)


def test_get_doctors_without_token():
    response = client.get("/doctors/")

    assert response.status_code == 401


def test_get_doctor_not_found():
    response = client.get(
        "/doctors/999999",
        headers={
            "Authorization": "Bearer invalid_token"
        }
    )

    assert response.status_code in [401, 403]
    
def test_get_doctors_with_admin_token(client, admin_token):
    response = client.get(
        "/doctors/",
        headers={
            "Authorization": f"Bearer {admin_token}"
        }
    )

    assert response.status_code == 200
    assert "data" in response.json()



def test_create_doctor_with_admin_token(client, admin_token):

    user_email = f"doctor_user_{uuid4().hex}@example.com"
    doctor_email = f"doctor_api_{uuid4().hex}@example.com"

    register_response = client.post(
        "/auth/register",
        json={
            "name": f"Doctor Test User {uuid4().hex}",
            "email": user_email,
            "password": "Doctor@123",
            "role": "Doctor"
        }
    )

    assert register_response.status_code in [200, 201]

    user_id = register_response.json()["user_id"]

    response = client.post(
        "/doctors/",
        headers={"Authorization": f"Bearer {admin_token}"},
        json={
            "name": "Test Doctor API",
            "specialization": "Cardiology",
            "email": doctor_email,
            "user_id": user_id
        }
    )

    assert response.status_code in [200, 201]
    
def test_doctor_cannot_create_doctor(client, doctor_token):
    response = client.post(
        "/doctors/",
        headers={
            "Authorization": f"Bearer {doctor_token}"
        },
        json={
            "name": "Unauthorized Doctor",
            "specialization": "Cardiology",
            "email": "unauthorizeddoctor@example.com",
            "user_id": 999
        }
    )

    assert response.status_code == 403


def test_doctor_can_view_doctors(client, doctor_token):
    response = client.get(
        "/doctors/",
        headers={
            "Authorization": f"Bearer {doctor_token}"
        }
    )

    assert response.status_code == 200
    assert "data" in response.json()
    
def test_doctor_cannot_update_doctor(client, doctor_token):
    response = client.put(
        "/doctors/1",
        headers={
            "Authorization": f"Bearer {doctor_token}"
        },
        json={
            "name": "Updated Doctor",
            "specialization": "Neurology",
            "email": "updateddoctor@example.com"
        }
    )

    assert response.status_code == 403


def test_doctor_cannot_patch_doctor(client, doctor_token):
    response = client.patch(
        "/doctors/1",
        headers={
            "Authorization": f"Bearer {doctor_token}"
        },
        json={
            "specialization": "Neurology"
        }
    )

    assert response.status_code == 403


def test_doctor_cannot_delete_doctor(client, doctor_token):
    response = client.delete(
        "/doctors/1",
        headers={
            "Authorization": f"Bearer {doctor_token}"
        }
    )

    assert response.status_code == 403