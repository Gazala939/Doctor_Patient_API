from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from db import get_db
from models.patient import Patient
from models.doctor import Doctor
from schemas.patient import PatientCreate, PatientUpdate, PatientPatch
from auth.jwt import verify_token
from services.patient_service import (
    get_patient_by_id,
    create_patient as create_patient_service,
    update_patient as update_patient_service,
    patch_patient as patch_patient_service,
    delete_patient as delete_patient_service,
    get_patients as get_patients_service

)

router = APIRouter(
    prefix="/patients",
    tags=["Patients"]
)

@router.post("/")
def create_patient(
    patient: PatientCreate,
    db: Session = Depends(get_db),
    payload: dict = Depends(verify_token)
):

    # Check whether doctor exists
    doctor = db.query(Doctor).filter(
        Doctor.id == patient.doctor_id
    ).first()

    if not doctor:
        raise HTTPException(
            status_code=404,
            detail="Doctor not found"
        )

    # Check whether doctor is active
    if not doctor.is_active:
        raise HTTPException(
            status_code=400,
            detail="Cannot assign patient to an inactive doctor"
        )

    # Create patient
    new_patient = create_patient_service(
        db=db,
        name=patient.name,
        age=patient.age,
        phone=patient.phone,
        doctor_id=patient.doctor_id
)

    return {
        "message": "Patient created successfully",
        "patient_id": new_patient.id,
        "doctor_id": new_patient.doctor_id
    }
    
@router.put("/{patient_id}")
def update_patient(
    patient_id: int,
    patient_data: PatientUpdate,
    db: Session = Depends(get_db),
    payload: dict = Depends(verify_token)
):

    # Only Admin can update patients
    if payload["role"] != "Admin":
        raise HTTPException(
            status_code=403,
            detail="Only Admin can update patients"
        )

    # Find patient
    patient = db.query(Patient).filter(
        Patient.id == patient_id
    ).first()

    if not patient:
        raise HTTPException(
            status_code=404,
            detail="Patient not found"
        )

    # Check doctor
    doctor = db.query(Doctor).filter(
        Doctor.id == patient_data.doctor_id
    ).first()

    if not doctor:
        raise HTTPException(
            status_code=404,
            detail="Doctor not found"
        )

    # Cannot assign patient to inactive doctor
    if not doctor.is_active:
        raise HTTPException(
            status_code=400,
            detail="Cannot assign patient to an inactive doctor"
        )

    # Update patient
    patient = update_patient_service(
        db=db,
        patient=patient,
        name=patient_data.name,
        age=patient_data.age,
        phone=patient_data.phone,
        doctor_id=patient_data.doctor_id
    )

    return {
        "message": "Patient updated successfully",
        "patient_id": patient.id,
        "doctor_id": patient.doctor_id
    }

@router.patch("/{patient_id}")
def patch_patient(
    patient_id: int,
    patient_data: PatientPatch,
    db: Session = Depends(get_db),
    payload: dict = Depends(verify_token)
):

    # Only Admin can update patients
    if payload["role"] != "Admin":
        raise HTTPException(
            status_code=403,
            detail="Only Admin can update patients"
        )

    # Find patient
    patient = db.query(Patient).filter(
        Patient.id == patient_id
    ).first()

    if not patient:
        raise HTTPException(
            status_code=404,
            detail="Patient not found"
        )

   
    # Update doctor if provided
    if patient_data.doctor_id is not None:

        doctor = db.query(Doctor).filter(
            Doctor.id == patient_data.doctor_id
        ).first()

        if not doctor:
            raise HTTPException(
                status_code=404,
                detail="Doctor not found"
            )

        if not doctor.is_active:
            raise HTTPException(
                status_code=400,
                detail="Cannot assign patient to an inactive doctor"
            )

    patient = patch_patient_service(
        db=db,
        patient=patient,
        name=patient_data.name,
        age=patient_data.age,
        phone=patient_data.phone,
        doctor_id=patient_data.doctor_id
        )
    return {
        "message": "Patient partially updated successfully",
        "patient_id": patient.id,
        "doctor_id": patient.doctor_id
    }

@router.delete("/{patient_id}")
def delete_patient(
    patient_id: int,
    db: Session = Depends(get_db),
    payload: dict = Depends(verify_token)
):

    # Only Admin can delete patients
    if payload["role"] != "Admin":
        raise HTTPException(
            status_code=403,
            detail="Only Admin can delete patients"
        )

    # Find patient
    patient = db.query(Patient).filter(
        Patient.id == patient_id
    ).first()

    if not patient:
        raise HTTPException(
            status_code=404,
            detail="Patient not found"
        )

    # Soft delete
    patient = delete_patient_service(
        db=db,
        patient=patient
    )

    return {
        "message": "Patient deactivated successfully",
        "patient_id": patient.id
    }
    
@router.get("/")
def get_patients(
    age_gt: int = None,
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    payload: dict = Depends(verify_token)
):

    # Calculate offset
    offset = (page - 1) * limit

    # Get patients from service
    total, patients = get_patients_service(
        db=db,
        age_gt=age_gt,
        offset=offset,
        limit=limit
    )

    # Return paginated response
    return {
        "total": total,
        "page": page,
        "limit": limit,
        "data": patients
    }
    
    
@router.get("/{patient_id}")
def get_patient(
    patient_id: int,
    db: Session = Depends(get_db),
    payload: dict = Depends(verify_token)
):

    patient = get_patient_by_id(
        db,
        patient_id
    )

    if not patient:
        raise HTTPException(
            status_code=404,
            detail="Patient not found"
        )

    # Admin can view any patient
    if payload["role"] == "Admin":
        return patient

    # Doctor can view only their assigned patients
    if payload["role"] == "Doctor":

        doctor = db.query(Doctor).filter(
            Doctor.user_id == payload["user_id"]
        ).first()

        if not doctor:
            raise HTTPException(
                status_code=404,
                detail="Doctor profile not found"
            )

        if patient.doctor_id != doctor.id:
            raise HTTPException(
                status_code=403,
                detail="Doctors can only view their assigned patients"
            )

        return patient

    raise HTTPException(
        status_code=403,
        detail="You are not authorized to view this patient"
    )