from sqlalchemy.orm import Session
from models.appointment import Appointment
from services.db_exception import handle_database_error
from datetime import datetime

def create_appointment(
    db: Session,
    doctor_id: int,
    patient_id: int,
    appointment_date,
    status,
    user_id: int
):
    appointment = Appointment(
        doctor_id=doctor_id,
        patient_id=patient_id,
        appointment_date=appointment_date,
        status=status,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
        created_by=user_id,
        updated_by=user_id
    )

    try:
        db.add(appointment)
        db.commit()
        db.refresh(appointment)

    except Exception as error:
        handle_database_error(db, error)

    return appointment


def get_appointment_by_id(
    db: Session,
    appointment_id: int
):
    return db.query(Appointment).filter(
        Appointment.id == appointment_id
    ).first()


def get_appointments(
    db: Session
):
    return db.query(Appointment).all()


def update_appointment(
    db: Session,
    appointment,
    doctor_id: int,
    patient_id: int,
    appointment_date,
    status,
    user_id: int
):
    appointment.doctor_id = doctor_id
    appointment.patient_id = patient_id
    appointment.appointment_date = appointment_date
    appointment.status = status

    appointment.updated_at = datetime.utcnow()
    appointment.updated_by = user_id

    try:
        db.commit()
        db.refresh(appointment)

    except Exception as error:
        handle_database_error(db, error)

    return appointment


def delete_appointment(
    db: Session,
    appointment
):
    try:
        db.delete(appointment)
        db.commit()

    except Exception as error:
        handle_database_error(db, error)

    return appointment


def get_doctor_appointments(
    db: Session,
    doctor_id: int
):
    return db.query(Appointment).filter(
        Appointment.doctor_id == doctor_id
    ).all()


def get_patient_appointments(
    db: Session,
    patient_id: int
):
    return db.query(Appointment).filter(
        Appointment.patient_id == patient_id
    ).all()