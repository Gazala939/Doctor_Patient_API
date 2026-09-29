from sqlalchemy.orm import Session
from models.doctor import Doctor
from models.patient import Patient
from datetime import datetime


def get_doctor_by_id(
    db: Session,
    doctor_id: int
):
    return db.query(Doctor).filter(
        Doctor.id == doctor_id
    ).first()


def create_doctor(
    db: Session,
    user_id: int,
    name: str,
    specialization: str,
    email: str,
    created_by: int
):
    current_time = datetime.utcnow()

    new_doctor = Doctor(
        user_id=user_id,
        name=name,
        specialization=specialization,
        email=email,
        created_at=current_time,
        updated_at=current_time,
        created_by=created_by,
        updated_by=created_by
    )

    db.add(new_doctor)
    db.commit()
    db.refresh(new_doctor)

    return new_doctor


def update_doctor(
    db: Session,
    doctor,
    name: str,
    specialization: str,
    email: str,
    user_id: int
):
    doctor.name = name
    doctor.specialization = specialization
    doctor.email = email

    doctor.updated_at = datetime.utcnow()
    doctor.updated_by = user_id

    db.commit()
    db.refresh(doctor)

    return doctor


def patch_doctor(
    db: Session,
    doctor,
    name=None,
    specialization=None,
    email=None,
    user_id: int = None
):
    if name is not None:
        doctor.name = name

    if specialization is not None:
        doctor.specialization = specialization

    if email is not None:
        doctor.email = email

    doctor.updated_at = datetime.utcnow()
    doctor.updated_by = user_id

    db.commit()
    db.refresh(doctor)

    return doctor


def delete_doctor(
    db: Session,
    doctor,
    user_id: int
):
    doctor.is_active = False

    doctor.updated_at = datetime.utcnow()
    doctor.updated_by = user_id

    db.commit()
    db.refresh(doctor)

    return doctor


def assign_patient(
    db: Session,
    doctor,
    patient
):
    patient.doctor_id = doctor.id

    db.commit()
    db.refresh(patient)

    return patient


def get_doctor_patients(
    db: Session,
    doctor_id: int
):
    return db.query(Patient).filter(
        Patient.doctor_id == doctor_id
    ).all()