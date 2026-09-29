from fastapi.testclient import TestClient

from index import app


client = TestClient(app)


def test_get_patients_without_token():
    response = client.get("/patients/")
    assert response.status_code == 401


def test_get_patient_not_found_without_token():
    response = client.get("/patients/999999")
    assert response.status_code == 401


def test_create_patient_without_token():
    response = client.post(
        "/patients/",
        json={
            "name": "Test Patient",
            "age": 30,
            "phone": "9876543210",
            "doctor_id": 1
        }
    )

    assert response.status_code == 401
    
def test_get_patients_with_admin_token(client, admin_token):
    response = client.get(
        "/patients/",
        headers={
            "Authorization": f"Bearer {admin_token}"
        }
    )

    assert response.status_code == 200
    assert "data" in response.json()


def test_get_patient_not_found_with_admin_token(client, admin_token):
    response = client.get(
        "/patients/999999",
        headers={
            "Authorization": f"Bearer {admin_token}"
        }
    )

    assert response.status_code == 404


def test_create_patient_with_admin_token(client, admin_token):
    response = client.post(
        "/patients/",
        headers={
            "Authorization": f"Bearer {admin_token}"
        },
        json={
            "name": "Test Patient API",
            "age": 30,
            "phone": "9876543210",
            "doctor_id": 1
        }
    )

    assert response.status_code in [200, 400, 404]
    
def test_doctor_cannot_create_patient(client, doctor_token):
    response = client.post(
        "/patients/",
        headers={
            "Authorization": f"Bearer {doctor_token}"
        },
        json={
            "name": "Unauthorized Patient",
            "age": 30,
            "phone": "9876543210",
            "doctor_id": 1
        }
    )

    assert response.status_code == 403


def test_doctor_can_view_patients(client, doctor_token):
    response = client.get(
        "/patients/",
        headers={
            "Authorization": f"Bearer {doctor_token}"
        }
    )

    assert response.status_code == 200
    assert "data" in response.json()
    
def test_doctor_cannot_update_patient(client, doctor_token):
    response = client.put(
        "/patients/1",
        headers={
            "Authorization": f"Bearer {doctor_token}"
        },
        json={
            "name": "Updated Patient",
            "age": 35,
            "phone": "9876543210",
            "doctor_id": 1
        }
    )

    assert response.status_code == 403


def test_doctor_cannot_patch_patient(client, doctor_token):
    response = client.patch(
        "/patients/1",
        headers={
            "Authorization": f"Bearer {doctor_token}"
        },
        json={
            "age": 36
        }
    )

    assert response.status_code == 403


def test_doctor_cannot_delete_patient(client, doctor_token):
    response = client.delete(
        "/patients/1",
        headers={
            "Authorization": f"Bearer {doctor_token}"
        }
    )

    assert response.status_code == 403
    
def test_create_patient_invalid_age(client, admin_token):
    response = client.post(
        "/patients/",
        headers={
            "Authorization": f"Bearer {admin_token}"
        },
        json={
            "name": "Invalid Patient",
            "age": 0,
            "phone": "9876543210",
            "doctor_id": 1
        }
    )

    assert response.status_code == 422
    
def test_create_patient_invalid_phone(client, admin_token):
    response = client.post(
        "/patients/",
        headers={
            "Authorization": f"Bearer {admin_token}"
        },
        json={
            "name": "Invalid Phone Patient",
            "age": 30,
            "phone": "123",
            "doctor_id": 1
        }
    )

    assert response.status_code == 422