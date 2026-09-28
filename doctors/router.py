from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from db import get_db
from models.doctor import Doctor
from schemas.doctor import DoctorCreate, DoctorUpdate, DoctorPatch
from auth.jwt import verify_token
from models.patient import Patient
from services.doctor_service import (
    get_doctor_by_id,
    create_doctor  as create_doctor_service,
    update_doctor as update_doctor_service,
    patch_doctor as patch_doctor_service,
    delete_doctor as delete_doctor_service,
    assign_patient,
    get_doctor_patients as get_doctor_patients_service
)

router = APIRouter(
    prefix="/doctors",
    tags=["Doctors"]
)


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

    new_doctor = create_doctor_service(
        db=db,
        user_id=doctor.user_id,
        name=doctor.name,
        specialization=doctor.specialization,
        email=doctor.email
    )

    return {
        "message": "Doctor created successfully",
        "doctor_id": new_doctor.id
    }

  
# get all doctors / filter / pagination
@router.get("/")
def get_doctors(
    specialization: str = None,
    is_active: bool = None,
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    payload: dict = Depends(verify_token)
):

    query = db.query(Doctor)

    # filter by specialization
    if specialization:
        query = query.filter(
            Doctor.specialization == specialization
        )

    # filter by active status
    if is_active is not None:
        query = query.filter(
            Doctor.is_active == is_active
        )
        
    total = query.count()

    # pagination
    offset = (page - 1) * limit

    doctors = query.offset(offset).limit(limit).all()

    return {
        "total": total,
        "page": page,
        "limit": limit,
        "data": doctors
    }

# get doctor by id
@router.get("/{doctor_id}")
def get_doctor(
    doctor_id: int,
    db: Session = Depends(get_db),
    payload: dict = Depends(verify_token)
):

    doctor = get_doctor_by_id(
        db,
        doctor_id
    )

    if not doctor:
        raise HTTPException(
            status_code=404,
            detail="Doctor not found"
        )

    return doctor

# update doctor
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
        
    existing_doctor = db.query(Doctor).filter(
        Doctor.email == doctor_data.email,
        Doctor.id != doctor_id
    ).first()

    if existing_doctor:
        raise HTTPException(
            status_code=400,
            detail="Doctor email already exists"
        )

    doctor = update_doctor_service(
        db=db,
        doctor=doctor,
        name=doctor_data.name,
        specialization=doctor_data.specialization,
        email=doctor_data.email
    ) 

    return {
        "message": "Doctor updated successfully",
        "doctor_id": doctor.id
    }
    
# update doctor -patch
@router.patch("/{doctor_id}")
def patch_doctor(
    doctor_id: int,
    doctor_data: DoctorPatch,
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

    # Check duplicate email
    if doctor_data.email is not None:

        existing_doctor = db.query(Doctor).filter(
            Doctor.email == doctor_data.email,
            Doctor.id != doctor_id
        ).first()

        if existing_doctor:
            raise HTTPException(
                status_code=400,
                detail="Doctor email already exists"
            )

    # Update using service
    doctor = patch_doctor_service(
        db=db,
        doctor=doctor,
        name=doctor_data.name,
        specialization=doctor_data.specialization,
        email=doctor_data.email
    )

    return {
        "message": "Doctor partially updated successfully",
        "doctor_id": doctor.id
    }
  
# delete doctor:soft delete
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

    doctor = delete_doctor_service(
        db=db,
        doctor=doctor
    )

    return {
        "message": "Doctor deactivated successfully",
        "doctor_id": doctor.id
    }

# assisn patient to doctor:
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
        
    if not doctor.is_active:
        raise HTTPException(
            status_code=400,
            detail="Cannot assign patient to an inactive doctor"
        )

    patient = db.query(Patient).filter(
        Patient.id == patient_id
    ).first()

    if not patient:
        raise HTTPException(
            status_code=404,
            detail="Patient not found"
        )

    patient = assign_patient(
        db=db,
        doctor=doctor,
        patient=patient
    )

    return {
        "message": "Patient assigned to doctor successfully",
        "doctor_id": doctor_id,
        "patient_id": patient_id
    }
    
# get all patients of doctor
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
        
    if not doctor.is_active:
        raise HTTPException(
           status_code=400,
           detail="Doctor is inactive"
        ) 
# doctor can only see their own patients
    if payload["role"] == "Doctor":
        if doctor.user_id != payload["user_id"]:
            raise HTTPException(
                status_code=403,
                detail="Doctors can only view their own patients"
            )

    patients = get_doctor_patients_service(
        db=db,
        doctor_id=doctor_id
    )

    return patients