from sqlalchemy.orm import Session
from models.patient import Patient
from datetime import datetime


def get_patient_by_id(
    db: Session,
    patient_id: int
):
    return db.query(Patient).filter(
        Patient.id == patient_id
    ).first()


def create_patient(
    db: Session,
    name: str,
    age: int,
    phone: str,
    doctor_id: int,
    user_id: int
):
    current_time = datetime.utcnow()

    new_patient = Patient(
        name=name,
        age=age,
        phone=phone,
        doctor_id=doctor_id,
        created_at=current_time,
        updated_at=current_time,
        created_by=user_id,
        updated_by=user_id
    )

    db.add(new_patient)
    db.commit()
    db.refresh(new_patient)

    return new_patient


def update_patient(
    db: Session,
    patient,
    name: str,
    age: int,
    phone: str,
    doctor_id: int,
    user_id: int
):
    patient.name = name
    patient.age = age
    patient.phone = phone
    patient.doctor_id = doctor_id

    patient.updated_at = datetime.utcnow()
    patient.updated_by = user_id

    db.commit()
    db.refresh(patient)

    return patient


def patch_patient(
    db: Session,
    patient,
    name=None,
    age=None,
    phone=None,
    doctor_id=None,
    user_id: int = None
):
    if name is not None:
        patient.name = name

    if age is not None:
        patient.age = age

    if phone is not None:
        patient.phone = phone

    if doctor_id is not None:
        patient.doctor_id = doctor_id

    patient.updated_at = datetime.utcnow()
    patient.updated_by = user_id

    db.commit()
    db.refresh(patient)

    return patient


def delete_patient(
    db: Session,
    patient,
    user_id: int
):
    patient.is_active = False

    patient.updated_at = datetime.utcnow()
    patient.updated_by = user_id

    db.commit()
    db.refresh(patient)

    return patient


def get_patients(
    db: Session,
    age_gt=None,
    doctor_id=None,
    offset=0,
    limit=10
):
    query = db.query(Patient)

    if age_gt is not None:
        query = query.filter(
            Patient.age > age_gt
        )

    if doctor_id is not None:
        query = query.filter(
            Patient.doctor_id == doctor_id
        )

    total = query.count()

    patients = query.offset(offset).limit(limit).all()

    return total, patients