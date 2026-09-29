from unittest.mock import MagicMock

from services.patient_service import (
    get_patient_by_id,
    create_patient,
    update_patient,
    patch_patient,
    delete_patient,
    get_patients,
)

from services.doctor_service import (
    get_doctor_by_id,
    create_doctor,
    update_doctor,
    patch_doctor,
    delete_doctor,
    assign_patient,
    get_doctor_patients,
)

from services.appointment_service import (
    get_appointment_by_id,
    create_appointment,
    get_appointments,
    update_appointment,
    delete_appointment,
    get_doctor_appointments,
    get_patient_appointments,
)

from sqlalchemy.exc import IntegrityError
from services.db_exception import handle_database_error
import pytest

def test_get_patient_by_id_is_callable():
    assert callable(get_patient_by_id)


def test_get_doctor_by_id_is_callable():
    assert callable(get_doctor_by_id)


def test_get_appointment_by_id_is_callable():
    assert callable(get_appointment_by_id)


def test_patient_service_functions_are_callable():
    assert callable(create_patient)
    assert callable(update_patient)
    assert callable(patch_patient)
    assert callable(delete_patient)
    assert callable(get_patients)


def test_doctor_service_functions_are_callable():
    assert callable(create_doctor)
    assert callable(update_doctor)
    assert callable(patch_doctor)
    assert callable(delete_doctor)
    assert callable(assign_patient)
    assert callable(get_doctor_patients)


def test_appointment_service_functions_are_callable():
    assert callable(create_appointment)
    assert callable(get_appointments)
    assert callable(update_appointment)
    assert callable(delete_appointment)
    assert callable(get_doctor_appointments)
    assert callable(get_patient_appointments)
    
def test_create_patient_service():
    db = MagicMock()

    patient = create_patient(
        db=db,
        name="Service Patient",
        age=30,
        phone="9876543210",
        doctor_id=1,
        user_id=1
    )

    db.add.assert_called_once()
    db.commit.assert_called_once()
    db.refresh.assert_called_once_with(patient)


def test_update_patient_service():
    db = MagicMock()
    patient = MagicMock()

    result = update_patient(
        db=db,
        patient=patient,
        name="Updated Patient",
        age=35,
        phone="9876543211",
        doctor_id=1,
        user_id=1
    )

    assert result == patient
    assert patient.name == "Updated Patient"
    assert patient.age == 35
    assert patient.phone == "9876543211"
    assert patient.doctor_id == 1
    db.commit.assert_called_once()


def test_patch_patient_service():
    db = MagicMock()
    patient = MagicMock()

    result = patch_patient(
        db=db,
        patient=patient,
        name="Patched Patient",
        age=40,
        phone="9876543212",
        doctor_id=1,
        user_id=1
    )

    assert result == patient
    assert patient.name == "Patched Patient"
    assert patient.age == 40
    assert patient.phone == "9876543212"
    assert patient.doctor_id == 1
    db.commit.assert_called_once()


def test_delete_patient_service():
    db = MagicMock()
    patient = MagicMock()

    result = delete_patient(
        db=db,
        patient=patient,
        user_id=1
    )

    assert result == patient
    assert patient.is_active is False
    db.commit.assert_called_once()
    
def test_get_patient_by_id_service():
    db = MagicMock()

    patient = MagicMock()
    db.query.return_value.filter.return_value.first.return_value = patient

    result = get_patient_by_id(db, 1)

    assert result == patient


def test_get_patients_service():
    db = MagicMock()

    query = db.query.return_value
    query.count.return_value = 2
    query.offset.return_value.limit.return_value.all.return_value = [
        MagicMock(),
        MagicMock()
    ]

    total, patients = get_patients(
        db=db,
        offset=0,
        limit=10
    )

    assert total == 2
    assert len(patients) == 2
    
def test_create_doctor_service():
    db = MagicMock()

    doctor = create_doctor(
        db=db,
        user_id=2,
        name="Service Doctor",
        specialization="Cardiology",
        email="service_doctor@example.com",
        created_by=1
    )

    db.add.assert_called_once()
    db.commit.assert_called_once()
    db.refresh.assert_called_once_with(doctor)


def test_update_doctor_service():
    db = MagicMock()
    doctor = MagicMock()

    result = update_doctor(
        db=db,
        doctor=doctor,
        name="Updated Doctor",
        specialization="Neurology",
        email="updated_doctor@example.com",
        user_id=1
    )

    assert result == doctor
    assert doctor.name == "Updated Doctor"
    assert doctor.specialization == "Neurology"
    assert doctor.email == "updated_doctor@example.com"
    db.commit.assert_called_once()


def test_patch_doctor_service():
    db = MagicMock()
    doctor = MagicMock()

    result = patch_doctor(
        db=db,
        doctor=doctor,
        name="Patched Doctor",
        specialization="Dermatology",
        email="patched_doctor@example.com",
        user_id=1
    )

    assert result == doctor
    assert doctor.name == "Patched Doctor"
    assert doctor.specialization == "Dermatology"
    assert doctor.email == "patched_doctor@example.com"
    db.commit.assert_called_once()


def test_delete_doctor_service():
    db = MagicMock()
    doctor = MagicMock()

    result = delete_doctor(
        db=db,
        doctor=doctor,
        user_id=1
    )

    assert result == doctor
    assert doctor.is_active is False
    db.commit.assert_called_once()
    
def test_get_doctor_by_id_service():
    db = MagicMock()

    doctor = MagicMock()
    db.query.return_value.filter.return_value.first.return_value = doctor

    result = get_doctor_by_id(db, 1)

    assert result == doctor


def test_assign_patient_service():
    db = MagicMock()
    doctor = MagicMock()
    doctor.id = 1
    patient = MagicMock()

    result = assign_patient(
        db=db,
        doctor=doctor,
        patient=patient
    )

    assert result == patient
    assert patient.doctor_id == 1
    db.commit.assert_called_once()
    db.refresh.assert_called_once_with(patient)


def test_get_doctor_patients_service():
    db = MagicMock()

    patients = [MagicMock(), MagicMock()]
    db.query.return_value.filter.return_value.all.return_value = patients

    result = get_doctor_patients(db, 1)

    assert result == patients
    
def test_create_appointment_service():
    db = MagicMock()

    appointment = create_appointment(
        db=db,
        doctor_id=1,
        patient_id=1,
        appointment_date="2026-10-01T10:00:00",
        status="scheduled",
        user_id=1
    )

    db.add.assert_called_once()
    db.commit.assert_called_once()
    db.refresh.assert_called_once_with(appointment)


def test_get_appointments_service():
    db = MagicMock()

    appointments = [MagicMock(), MagicMock()]
    db.query.return_value.all.return_value = appointments

    result = get_appointments(db)

    assert result == appointments


def test_update_appointment_service():
    db = MagicMock()
    appointment = MagicMock()

    result = update_appointment(
        db=db,
        appointment=appointment,
        doctor_id=2,
        patient_id=3,
        appointment_date="2026-10-02T11:00:00",
        status="completed",
        user_id=1
    )

    assert result == appointment
    assert appointment.doctor_id == 2
    assert appointment.patient_id == 3
    assert appointment.appointment_date == "2026-10-02T11:00:00"
    assert appointment.status == "completed"
    db.commit.assert_called_once()


def test_delete_appointment_service():
    db = MagicMock()
    appointment = MagicMock()

    result = delete_appointment(
        db=db,
        appointment=appointment
    )

    assert result == appointment
    db.delete.assert_called_once_with(appointment)
    db.commit.assert_called_once()


def test_get_doctor_appointments_service():
    db = MagicMock()

    appointments = [MagicMock(), MagicMock()]
    db.query.return_value.filter.return_value.all.return_value = appointments

    result = get_doctor_appointments(db, 1)

    assert result == appointments


def test_get_patient_appointments_service():
    db = MagicMock()

    appointments = [MagicMock()]
    db.query.return_value.filter.return_value.all.return_value = appointments

    result = get_patient_appointments(db, 1)

    assert result == appointments
    

def test_handle_database_integrity_error():
    db = MagicMock()

    error = IntegrityError(
        statement="INSERT",
        params={},
        orig=Exception("duplicate")
    )

    with pytest.raises(Exception):
        handle_database_error(db, error)

    db.rollback.assert_called_once()