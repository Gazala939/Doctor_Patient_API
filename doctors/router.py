from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from db import SessionLocal
from models.doctor import Doctor
from schemas.doctor import DoctorCreate, DoctorUpdate
from auth.jwt import verify_token
from models.patient import Patient

router = APIRouter(
    prefix="/doctors",
    tags=["Doctors"]
)


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@router.post("/")
def create_doctor(
    doctor: DoctorCreate,
    db: Session = Depends(get_db),
    payload: dict = Depends(verify_token)
):

    if payload["role"] != "Admin":
        raise HTTPException(
            status_code=403,
            detail="Only Admin can create doctors"
        )

    existing_doctor = db.query(Doctor).filter(
        Doctor.email == doctor.email
    ).first()

    if existing_doctor:
        raise HTTPException(
            status_code=400,
            detail="Doctor email already exists"
        )

    new_doctor = Doctor(
        user_id=doctor.user_id,
        name=doctor.name,
        specialization=doctor.specialization,
        email=doctor.email
    )

    db.add(new_doctor)
    db.commit()
    db.refresh(new_doctor)

    return {
        "message": "Doctor created successfully",
        "doctor_id": new_doctor.id
    }
    
@router.get("/")
def get_doctors(
    db: Session = Depends(get_db),
    payload: dict = Depends(verify_token)
):

    doctors = db.query(Doctor).all()

    return doctors

@router.get("/{doctor_id}")
def get_doctor(
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

    return doctor

@router.put("/{doctor_id}")
def update_doctor(
    doctor_id: int,
    doctor_data: DoctorUpdate,
    db: Session = Depends(get_db),
    payload: dict = Depends(verify_token)
):

    if payload["role"] != "Admin":
        raise HTTPException(
            status_code=403,
            detail="Only Admin can update doctors"
        )

    doctor = db.query(Doctor).filter(
        Doctor.id == doctor_id
    ).first()

    if not doctor:
        raise HTTPException(
            status_code=404,
            detail="Doctor not found"
        )

    doctor.name = doctor_data.name
    doctor.specialization = doctor_data.specialization
    doctor.email = doctor_data.email

    db.commit()
    db.refresh(doctor)

    return {
        "message": "Doctor updated successfully",
        "doctor_id": doctor.id
    }
    
@router.delete("/{doctor_id}")
def delete_doctor(
    doctor_id: int,
    db: Session = Depends(get_db),
    payload: dict = Depends(verify_token)
):

    if payload["role"] != "Admin":
        raise HTTPException(
            status_code=403,
            detail="Only Admin can delete doctors"
        )

    doctor = db.query(Doctor).filter(
        Doctor.id == doctor_id
    ).first()

    if not doctor:
        raise HTTPException(
            status_code=404,
            detail="Doctor not found"
        )

    doctor.is_active = False

    db.commit()

    return {
        "message": "Doctor deactivated successfully",
        "doctor_id": doctor.id
    }

@router.post("/{doctor_id}/patients/{patient_id}")
def assign_patient_to_doctor(
    doctor_id: int,
    patient_id: int,
    db: Session = Depends(get_db),
    payload: dict = Depends(verify_token)
):
    if payload["role"] != "Admin":
        raise HTTPException(
            status_code=403,
            detail="Only Admin can assign patients"
        )

    doctor = db.query(Doctor).filter(
        Doctor.id == doctor_id
    ).first()

    if not doctor:
        raise HTTPException(
            status_code=404,
            detail="Doctor not found"
        )

    patient = db.query(Patient).filter(
        Patient.id == patient_id
    ).first()

    if not patient:
        raise HTTPException(
            status_code=404,
            detail="Patient not found"
        )

    patient.doctor_id = doctor_id

    db.commit()

    return {
        "message": "Patient assigned to doctor successfully",
        "doctor_id": doctor_id,
        "patient_id": patient_id
    }
    
@router.get("/{doctor_id}/patients")
def get_doctor_patients(
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

    if payload["role"] == "Doctor":
        if doctor.user_id != payload["user_id"]:
            raise HTTPException(
                status_code=403,
                detail="Doctors can only view their own patients"
            )

    patients = db.query(Patient).filter(
        Patient.doctor_id == doctor_id
    ).all()

    return patients