from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Query
)

from sqlalchemy.orm import Session
from sqlalchemy import func

from db import get_db

from models.billing import Billing
from models.doctor import Doctor
from models.patient import Patient

from schemas.billing import (
    BillingCreate,
    BillingUpdate,
    BillingPatch,
    BillingResponse
)

from services.billing_service import create_billing

from auth.jwt import verify_token

from datetime import datetime, date


router = APIRouter(
    prefix="",
    tags=["Billings"]
)


# ============================================================
# CREATE BILLING
# POST /billings
# ============================================================

@router.post(
    "/billings",
    response_model=BillingResponse
)
def create_billing_api(
    billing: BillingCreate,
    db: Session = Depends(get_db),
    current_user=Depends(verify_token)
):
    if current_user["role"] != "Admin":
        raise HTTPException(
            status_code=403,
            detail="Forbidden"
        )

    return create_billing(
        db=db,
        patient_id=billing.patient_id,
        doctor_id=billing.doctor_id,
        appointment_id=billing.appointment_id,
        consultation_fee=billing.consultation_fee,
        additional_charges=billing.additional_charges,
        payment_status=billing.payment_status,
        payment_mode=billing.payment_mode
    )


# ============================================================
# GET ALL BILLINGS
# GET /billings
# ============================================================

@router.get(
    "/billings",
    response_model=list[BillingResponse]
)
def get_billings(
    payment_status: str | None = Query(default=None),
    doctor_id: int | None = Query(default=None, gt=0),
    patient_id: int | None = Query(default=None, gt=0),
    from_date: datetime | None = Query(default=None),
    to_date: datetime | None = Query(default=None),

    page: int = Query(default=1, ge=1),
    limit: int = Query(default=10, ge=1, le=100),

    db: Session = Depends(get_db),
    current_user=Depends(verify_token)
):
    query = db.query(Billing).filter(
        Billing.is_active == True
    )

    # Payment status filter
    if payment_status is not None:
        query = query.filter(
            Billing.payment_status == payment_status
        )

    # Doctor filter
    if doctor_id is not None:
        query = query.filter(
            Billing.doctor_id == doctor_id
        )

    # Patient filter
    if patient_id is not None:
        query = query.filter(
            Billing.patient_id == patient_id
        )

    # From date filter
    if from_date is not None:
        query = query.filter(
            Billing.created_at >= from_date
        )

    # To date filter
    if to_date is not None:
        query = query.filter(
            Billing.created_at <= to_date
        )

    # Doctor authorization
    if current_user["role"] == "Doctor":

        doctor = db.query(Doctor).filter(
            Doctor.user_id == current_user["user_id"]
        ).first()

        if not doctor:
            raise HTTPException(
                status_code=404,
                detail="Doctor not found"
            )

        query = query.filter(
            Billing.doctor_id == doctor.id
        )

    elif current_user["role"] != "Admin":

        raise HTTPException(
            status_code=403,
            detail="Forbidden"
        )

    # Pagination
    offset = (page - 1) * limit

    billings = query.offset(
        offset
    ).limit(
        limit
    ).all()

    return billings


# ============================================================
# PATIENT BILLINGS
# GET /patients/{patient_id}/billings
# ============================================================

@router.get(
    "/patients/{patient_id}/billings",
    response_model=list[BillingResponse]
)
def get_patient_billings(
    patient_id: int,

    page: int = Query(
        default=1,
        ge=1
    ),

    limit: int = Query(
        default=10,
        ge=1,
        le=100
    ),

    db: Session = Depends(get_db),
    current_user=Depends(verify_token)
):
    patient = db.query(Patient).filter(
        Patient.id == patient_id
    ).first()

    if not patient:
        raise HTTPException(
            status_code=404,
            detail="Patient not found"
        )

    # Admin can view all patient billings
    if current_user["role"] == "Admin":
        pass

    # Doctor can view only their patient's billings
    elif current_user["role"] == "Doctor":

        doctor = db.query(Doctor).filter(
            Doctor.user_id == current_user["user_id"]
        ).first()

        if not doctor:
            raise HTTPException(
                status_code=404,
                detail="Doctor not found"
            )

        if patient.doctor_id != doctor.id:
            raise HTTPException(
                status_code=403,
                detail="Forbidden"
            )

    else:
        raise HTTPException(
            status_code=403,
            detail="Forbidden"
        )

    query = db.query(Billing).filter(
        Billing.patient_id == patient_id,
        Billing.is_active == True
    )

    offset = (page - 1) * limit

    billings = query.offset(
        offset
    ).limit(
        limit
    ).all()

    return billings


# ============================================================
# DOCTOR BILLINGS
# GET /doctors/{doctor_id}/billings
# ============================================================

@router.get(
    "/doctors/{doctor_id}/billings",
    response_model=list[BillingResponse]
)
def get_doctor_billings(
    doctor_id: int,

    page: int = Query(
        default=1,
        ge=1
    ),

    limit: int = Query(
        default=10,
        ge=1,
        le=100
    ),

    db: Session = Depends(get_db),
    current_user=Depends(verify_token)
):
    doctor = db.query(Doctor).filter(
        Doctor.id == doctor_id
    ).first()

    if not doctor:
        raise HTTPException(
            status_code=404,
            detail="Doctor not found"
        )

    query = db.query(Billing).filter(
        Billing.doctor_id == doctor_id,
        Billing.is_active == True
    )

    # Admin can view any doctor's billings
    if current_user["role"] == "Admin":
        pass

    # Doctor can view only their own billings
    elif current_user["role"] == "Doctor":

        current_doctor = db.query(Doctor).filter(
            Doctor.user_id == current_user["user_id"]
        ).first()

        if not current_doctor:
            raise HTTPException(
                status_code=404,
                detail="Doctor not found"
            )

        if current_doctor.id != doctor_id:
            raise HTTPException(
                status_code=403,
                detail="Forbidden"
            )

    else:
        raise HTTPException(
            status_code=403,
            detail="Forbidden"
        )

    offset = (page - 1) * limit

    billings = query.offset(
        offset
    ).limit(
        limit
    ).all()

    return billings


# ============================================================
# GET BILLING BY ID
# GET /billings/{billing_id}
# ============================================================

@router.get(
    "/billings/{billing_id}",
    response_model=BillingResponse
)
def get_billing(
    billing_id: int,

    db: Session = Depends(get_db),
    current_user=Depends(verify_token)
):
    billing = db.query(Billing).filter(
        Billing.id == billing_id,
        Billing.is_active == True
    ).first()

    if not billing:
        raise HTTPException(
            status_code=404,
            detail="Billing not found"
        )

    # Admin
    if current_user["role"] == "Admin":
        return billing

    # Doctor
    if current_user["role"] == "Doctor":

        doctor = db.query(Doctor).filter(
            Doctor.user_id == current_user["user_id"]
        ).first()

        if not doctor:
            raise HTTPException(
                status_code=404,
                detail="Doctor not found"
            )

        if billing.doctor_id != doctor.id:
            raise HTTPException(
                status_code=403,
                detail="Forbidden"
            )

        return billing

    raise HTTPException(
        status_code=403,
        detail="Forbidden"
    )


# ============================================================
# FULL UPDATE
# PUT /billings/{billing_id}
# ============================================================

@router.put(
    "/billings/{billing_id}",
    response_model=BillingResponse
)
def update_billing(
    billing_id: int,
    billing_data: BillingUpdate,

    db: Session = Depends(get_db),
    current_user=Depends(verify_token)
):
    if current_user["role"] != "Admin":
        raise HTTPException(
            status_code=403,
            detail="Forbidden"
        )

    billing = db.query(Billing).filter(
        Billing.id == billing_id,
        Billing.is_active == True
    ).first()

    if not billing:
        raise HTTPException(
            status_code=404,
            detail="Billing not found"
        )

    billing.consultation_fee = (
        billing_data.consultation_fee
    )

    billing.additional_charges = (
        billing_data.additional_charges
    )

    billing.total_amount = (
        billing_data.consultation_fee
        + billing_data.additional_charges
    )

    billing.payment_status = (
        billing_data.payment_status
    )

    billing.payment_mode = (
        billing_data.payment_mode
    )

    db.commit()
    db.refresh(billing)

    return billing


# ============================================================
# PARTIAL UPDATE
# PATCH /billings/{billing_id}
# ============================================================

@router.patch(
    "/billings/{billing_id}",
    response_model=BillingResponse
)
def patch_billing(
    billing_id: int,
    billing_data: BillingPatch,

    db: Session = Depends(get_db),
    current_user=Depends(verify_token)
):
    if current_user["role"] != "Admin":
        raise HTTPException(
            status_code=403,
            detail="Forbidden"
        )

    billing = db.query(Billing).filter(
        Billing.id == billing_id,
        Billing.is_active == True
    ).first()

    if not billing:
        raise HTTPException(
            status_code=404,
            detail="Billing not found"
        )

    if billing_data.consultation_fee is not None:
        billing.consultation_fee = (
            billing_data.consultation_fee
        )

    if billing_data.additional_charges is not None:
        billing.additional_charges = (
            billing_data.additional_charges
        )

    billing.total_amount = (
        billing.consultation_fee
        + billing.additional_charges
    )

    if billing_data.payment_status is not None:
        billing.payment_status = (
            billing_data.payment_status
        )

    if billing_data.payment_mode is not None:
        billing.payment_mode = (
            billing_data.payment_mode
        )

    db.commit()
    db.refresh(billing)

    return billing


# ============================================================
# SOFT DELETE
# DELETE /billings/{billing_id}
# ============================================================

@router.delete(
    "/billings/{billing_id}"
)
def delete_billing(
    billing_id: int,

    db: Session = Depends(get_db),
    current_user=Depends(verify_token)
):
    if current_user["role"] != "Admin":
        raise HTTPException(
            status_code=403,
            detail="Forbidden"
        )

    billing = db.query(Billing).filter(
        Billing.id == billing_id,
        Billing.is_active == True
    ).first()

    if not billing:
        raise HTTPException(
            status_code=404,
            detail="Billing not found"
        )

    billing.is_active = False

    db.commit()

    return {
        "message": "Billing deleted successfully",
        "billing_id": billing.id
    }


# ============================================================
# REVENUE REPORT
# GET /reports/revenue
# ============================================================

@router.get(
    "/reports/revenue"
)
def revenue_report(
    doctor_id: int | None = Query(
        default=None,
        gt=0
    ),

    from_date: date | None = Query(
        default=None,
        alias="from"
    ),

    to_date: date | None = Query(
        default=None,
        alias="to"
    ),

    db: Session = Depends(get_db),
    current_user=Depends(verify_token)
):
    # Only Admin and Doctor can access revenue reports
    if current_user["role"] not in [
        "Admin",
        "Doctor"
    ]:
        raise HTTPException(
            status_code=403,
            detail="Forbidden"
        )

    # Doctor authorization
    if current_user["role"] == "Doctor":

        doctor = db.query(Doctor).filter(
            Doctor.user_id == current_user["user_id"]
        ).first()

        if not doctor:
            raise HTTPException(
                status_code=404,
                detail="Doctor not found"
            )

        if doctor_id is not None and doctor_id != doctor.id:
            raise HTTPException(
                status_code=403,
                detail="Forbidden"
            )

        doctor_id = doctor.id

    # Validate date range
    if (
        from_date is not None
        and to_date is not None
        and from_date > to_date
    ):
        raise HTTPException(
            status_code=400,
            detail="From date cannot be greater than to date"
        )

    # Only active and paid billings count as revenue
    query = db.query(Billing).filter(
        Billing.is_active == True,
        Billing.payment_status == "paid"
    )

    # Doctor filter
    if doctor_id is not None:
        query = query.filter(
            Billing.doctor_id == doctor_id
        )

    # From date
    if from_date is not None:
        query = query.filter(
            Billing.created_at >= datetime.combine(
                from_date,
                datetime.min.time()
            )
        )

    # To date
    if to_date is not None:
        query = query.filter(
            Billing.created_at <= datetime.combine(
                to_date,
                datetime.max.time()
            )
        )

    # Total revenue
    total_revenue = query.with_entities(
        func.coalesce(
            func.sum(Billing.total_amount),
            0
        )
    ).scalar()

    # Revenue per doctor
    doctor_revenue = query.with_entities(
        Billing.doctor_id,
        func.sum(
            Billing.total_amount
        ).label("total_revenue")
    ).group_by(
        Billing.doctor_id
    ).all()

    revenue_per_doctor = []

    for item in doctor_revenue:
        revenue_per_doctor.append({
            "doctor_id": item.doctor_id,
            "total_revenue": item.total_revenue
        })

    # Revenue per day
    daily_revenue = query.with_entities(
        func.date(
            Billing.created_at
        ).label("date"),
        func.sum(
            Billing.total_amount
        ).label("total_revenue")
    ).group_by(
        func.date(Billing.created_at)
    ).order_by(
        func.date(Billing.created_at)
    ).all()

    revenue_per_day = []

    for item in daily_revenue:
        revenue_per_day.append({
            "date": item.date,
            "total_revenue": item.total_revenue
        })

    return {
        "total_revenue": total_revenue,
        "revenue_per_doctor": revenue_per_doctor,
        "revenue_per_day": revenue_per_day
    }