from fastapi.testclient import TestClient

from index import app


client = TestClient(app)


def test_get_appointments_without_token():
    response = client.get("/appointments/")

    assert response.status_code == 401


def test_get_appointment_not_found_without_token():
    response = client.get("/appointments/999999")

    assert response.status_code == 401


def test_create_appointment_without_token():
    response = client.post(
        "/appointments/",
        json={
            "doctor_id": 1,
            "patient_id": 1,
            "appointment_date": "2026-10-01T10:00:00",
            "status": "scheduled"
        }
    )

    assert response.status_code == 401
    
def test_get_appointments_with_admin_token(client, admin_token):
    response = client.get(
        "/appointments/",
        headers={
            "Authorization": f"Bearer {admin_token}"
        }
    )

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_appointment_not_found_with_admin_token(client, admin_token):
    response = client.get(
        "/appointments/999999",
        headers={
            "Authorization": f"Bearer {admin_token}"
        }
    )

    assert response.status_code == 404


def test_create_appointment_with_admin_token(client, admin_token):
    response = client.post(
        "/appointments/",
        headers={
            "Authorization": f"Bearer {admin_token}"
        },
        json={
            "doctor_id": 1,
            "patient_id": 1,
            "appointment_date": "2026-10-01T10:00:00",
            "status": "scheduled"
        }
    )

    assert response.status_code in [200, 400, 404]
    
def test_doctor_cannot_create_appointment(client, doctor_token):
    response = client.post(
        "/appointments/",
        headers={
            "Authorization": f"Bearer {doctor_token}"
        },
        json={
            "doctor_id": 1,
            "patient_id": 1,
            "appointment_date": "2026-10-02T10:00:00",
            "status": "scheduled"
        }
    )

    assert response.status_code == 403


def test_doctor_can_view_appointments(client, doctor_token):
    response = client.get(
        "/appointments/",
        headers={
            "Authorization": f"Bearer {doctor_token}"
        }
    )

    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_doctor_cannot_update_appointment(client, doctor_token):
    response = client.put(
        "/appointments/1",
        headers={
            "Authorization": f"Bearer {doctor_token}"
        },
        json={
            "doctor_id": 1,
            "patient_id": 1,
            "appointment_date": "2026-10-02T11:00:00",
            "status": "completed"
        }
    )

    assert response.status_code == 403


def test_doctor_cannot_delete_appointment(client, doctor_token):
    response = client.delete(
        "/appointments/1",
        headers={
            "Authorization": f"Bearer {doctor_token}"
        }
    )

    assert response.status_code == 403