from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from db import SessionLocal
from models.patient import Patient
from schemas.patient import PatientCreate
from auth.jwt import verify_token


router = APIRouter(
    prefix="/patients",
    tags=["Patients"]
)


def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


@router.post("/")
def create_patient(
    patient: PatientCreate,
    db: Session = Depends(get_db),
    payload: dict = Depends(verify_token)
):

    new_patient = Patient(
        name=patient.name,
        age=patient.age,
        phone=patient.phone
    )

    db.add(new_patient)
    db.commit()
    db.refresh(new_patient)

    return {
        "message": "Patient created successfully",
        "patient_id": new_patient.id
    }

@router.get("/")
def get_patients(
    db: Session = Depends(get_db),
    payload: dict = Depends(verify_token)
):
    if payload["role"] != "Admin":
        raise HTTPException(
            status_code=403,
            detail="Only Admin can view all patients"
        )

    patients = db.query(Patient).all()

    return patients


@router.get("/")
def get_patients(
    db: Session = Depends(get_db),
    payload: dict = Depends(verify_token)
):
    if payload["role"] == "Admin":
        patients = db.query(Patient).all()

        return patients

    if payload["role"] == "Doctor":
        patients = db.query(Patient).filter(
            Patient.doctor_id == payload["user_id"]
        ).all()

        return patients

    raise HTTPException(
        status_code=403,
        detail="You are not authorized to view patients"
    )
    
@router.get("/{patient_id}")
def get_patient(
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

    if payload["role"] == "Admin":
        return patient

    if payload["role"] == "Doctor":

        if patient.doctor_id != payload["user_id"]:
            raise HTTPException(
                status_code=403,
                detail="Doctors can only view their assigned patients"
            )

        return patient

    raise HTTPException(
        status_code=403,
        detail="You are not authorized to view this patient"
    )