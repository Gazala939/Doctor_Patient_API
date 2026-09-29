from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from db import get_db
from models.appointment import Appointment
from models.doctor import Doctor
from models.patient import Patient

from schemas.appointment import (
    AppointmentCreate,
    AppointmentUpdate,
    AppointmentResponse
)

from auth.jwt import verify_token

from services.appointment_service import (
    create_appointment as create_appointment_service,
    get_appointment_by_id,
    get_appointments as get_appointments_service,
    update_appointment as update_appointment_service,
    delete_appointment as delete_appointment_service,
    get_doctor_appointments as get_doctor_appointments_service,
    get_patient_appointments as get_patient_appointments_service
)


router = APIRouter(
    prefix="/appointments",
    tags=["Appointments"]
)


# Create appointment
@router.post(
    "/",
    summary="Create appointment",
    description="Creates a new appointment for a doctor and patient. Only Admin users are allowed."
)
def create_appointment(
    appointment: AppointmentCreate,
    db: Session = Depends(get_db),
    payload: dict = Depends(verify_token)
):

    # Only Admin can create appointments
    if payload["role"] != "Admin":
        raise HTTPException(
            status_code=403,
            detail="Only Admin can create appointments"
        )

    # Check doctor
    doctor = db.query(Doctor).filter(
        Doctor.id == appointment.doctor_id
    ).first()

    if not doctor:
        raise HTTPException(
            status_code=404,
            detail="Doctor not found"
        )

    # Check doctor active
    if not doctor.is_active:
        raise HTTPException(
            status_code=400,
            detail="Cannot create appointment with an inactive doctor"
        )

    # Check patient
    patient = db.query(Patient).filter(
        Patient.id == appointment.patient_id
    ).first()

    if not patient:
        raise HTTPException(
            status_code=404,
            detail="Patient not found"
        )

    # Check overlapping appointment
    existing_appointment = db.query(Appointment).filter(
        Appointment.doctor_id == appointment.doctor_id,
        Appointment.appointment_date == appointment.appointment_date,
        Appointment.status == "scheduled"
    ).first()

    if existing_appointment:
        raise HTTPException(
            status_code=400,
            detail="Doctor already has an appointment at this time"
        )

    # Create appointment
    new_appointment = create_appointment_service(
        db=db,
        doctor_id=appointment.doctor_id,
        patient_id=appointment.patient_id,
        appointment_date=appointment.appointment_date,
        status=appointment.status,
        user_id=payload["user_id"]
    )

    return new_appointment


# Get all appointments with pagination
@router.get(
    "/",
    summary="Get all appointments",
    description="Returns a paginated list of appointments."
)
def get_appointments(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    payload: dict = Depends(verify_token)
):

    appointments = db.query(Appointment).offset(
        skip
    ).limit(
        limit
    ).all()

    return appointments


# Get appointment by ID
@router.get(
    "/{appointment_id}",
    summary="Get appointment by ID",
    description="Returns details of a specific appointment."
)
def get_appointment(
    appointment_id: int,
    db: Session = Depends(get_db),
    payload: dict = Depends(verify_token)
):

    appointment = get_appointment_by_id(
        db=db,
        appointment_id=appointment_id
    )

    if not appointment:
        raise HTTPException(
            status_code=404,
            detail="Appointment not found"
        )

    return appointment


# Update appointment
@router.put(
    "/{appointment_id}",
    summary="Update appointment",
    description="Updates all details of an existing appointment. Only Admin users are allowed."
)
def update_appointment(
    appointment_id: int,
    appointment_data: AppointmentUpdate,
    db: Session = Depends(get_db),
    payload: dict = Depends(verify_token)
):

    # Only Admin can update appointments
    if payload["role"] != "Admin":
        raise HTTPException(
            status_code=403,
            detail="Only Admin can update appointments"
        )

    # Find appointment
    appointment = get_appointment_by_id(
        db=db,
        appointment_id=appointment_id
    )

    if not appointment:
        raise HTTPException(
            status_code=404,
            detail="Appointment not found"
        )

    # Check doctor
    doctor = db.query(Doctor).filter(
        Doctor.id == appointment_data.doctor_id
    ).first()

    if not doctor:
        raise HTTPException(
            status_code=404,
            detail="Doctor not found"
        )

    if not doctor.is_active:
        raise HTTPException(
            status_code=400,
            detail="Cannot assign appointment to an inactive doctor"
        )

    # Check patient
    patient = db.query(Patient).filter(
        Patient.id == appointment_data.patient_id
    ).first()

    if not patient:
        raise HTTPException(
            status_code=404,
            detail="Patient not found"
        )

    # Check overlapping appointment
    existing_appointment = db.query(Appointment).filter(
        Appointment.doctor_id == appointment_data.doctor_id,
        Appointment.appointment_date == appointment_data.appointment_date,
        Appointment.status == "scheduled",
        Appointment.id != appointment_id
    ).first()

    if existing_appointment:
        raise HTTPException(
            status_code=400,
            detail="Doctor already has an appointment at this time"
        )

    appointment = update_appointment_service(
        db=db,
        appointment=appointment,
        doctor_id=appointment_data.doctor_id,
        patient_id=appointment_data.patient_id,
        appointment_date=appointment_data.appointment_date,
        status=appointment_data.status,
        user_id=payload["user_id"]
    )

    return appointment


# Delete appointment
@router.delete(
    "/{appointment_id}",
    summary="Delete appointment",
    description="Deletes an existing appointment. Only Admin users are allowed."
)
def delete_appointment(
    appointment_id: int,
    db: Session = Depends(get_db),
    payload: dict = Depends(verify_token)
):

    # Only Admin can delete appointments
    if payload["role"] != "Admin":
        raise HTTPException(
            status_code=403,
            detail="Only Admin can delete appointments"
        )

    appointment = get_appointment_by_id(
        db=db,
        appointment_id=appointment_id
    )

    if not appointment:
        raise HTTPException(
            status_code=404,
            detail="Appointment not found"
        )

    delete_appointment_service(
        db=db,
        appointment=appointment
    )

    return {
        "message": "Appointment deleted successfully",
        "appointment_id": appointment_id
    }


# Get appointments by doctor
@router.get(
    "/doctor/{doctor_id}",
    summary="Get doctor's appointments",
    description="Returns all appointments associated with a specific doctor."
)
def get_doctor_appointments(
    doctor_id: int,
    db: Session = Depends(get_db),
    payload: dict = Depends(verify_token)
):

    doctor = db.query(Doctor).filter(
        Doctor.id == doctor_id
    ).first()

    if not doctor:
        raise HTTPException(
            status_code=404,
            detail="Doctor not found"
        )

    appointments = get_doctor_appointments_service(
        db=db,
        doctor_id=doctor_id
    )

    return appointments


# Get appointments by patient
@router.get(
    "/patient/{patient_id}",
    summary="Get patient's appointments",
    description="Returns all appointments associated with a specific patient."
)
def get_patient_appointments(
    patient_id: int,
    db: Session = Depends(get_db),
    payload: dict = Depends(verify_token)
):

    patient = db.query(Patient).filter(
        Patient.id == patient_id
    ).first()

    if not patient:
        raise HTTPException(
            status_code=404,
            detail="Patient not found"
        )

    appointments = get_patient_appointments_service(
        db=db,
        patient_id=patient_id
    )

    return appointments