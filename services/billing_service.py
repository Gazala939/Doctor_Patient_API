from fastapi import HTTPException
from sqlalchemy.orm import Session

from models.billing import Billing
from models.patient import Patient
from models.doctor import Doctor
from models.appointment import Appointment


def create_billing(
    db: Session,
    patient_id: int,
    doctor_id: int,
    appointment_id: int | None,
    consultation_fee: float,
    additional_charges: float,
    payment_status: str,
    payment_mode: str | None
):
    # --------------------------------------------------------
    # Check patient
    # --------------------------------------------------------

    patient = db.query(Patient).filter(
        Patient.id == patient_id,
        Patient.is_active == True
    ).first()

    if not patient:
        raise HTTPException(
            status_code=404,
            detail="Patient not found"
        )

    # --------------------------------------------------------
    # Check doctor
    # --------------------------------------------------------

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
            detail="Cannot create billing for an inactive doctor"
        )

    # --------------------------------------------------------
    # Check appointment
    # --------------------------------------------------------

    appointment = None

    if appointment_id is not None:

        appointment = db.query(Appointment).filter(
            Appointment.id == appointment_id
        ).first()

        if not appointment:
            raise HTTPException(
                status_code=404,
                detail="Appointment not found"
            )

        # Check patient
        if appointment.patient_id != patient_id:
            raise HTTPException(
                status_code=400,
                detail="Appointment does not belong to this patient"
            )

        # Check doctor
        if appointment.doctor_id != doctor_id:
            raise HTTPException(
                status_code=400,
                detail="Appointment does not belong to this doctor"
            )

        # Cancelled appointment cannot be billed
        if appointment.status.lower() == "cancelled":
            raise HTTPException(
                status_code=400,
                detail="Cannot create billing for a cancelled appointment"
            )

        # Check duplicate billing
        existing_billing = db.query(Billing).filter(
            Billing.appointment_id == appointment_id
        ).first()

        if existing_billing:
            raise HTTPException(
                status_code=400,
                detail="Billing already exists for this appointment"
            )

    # --------------------------------------------------------
    # Calculate total
    # --------------------------------------------------------

    total_amount = (
        consultation_fee
        + additional_charges
    )

    # --------------------------------------------------------
    # Database transaction
    # --------------------------------------------------------

    try:

        # Create billing
        billing = Billing(
            patient_id=patient_id,
            doctor_id=doctor_id,
            appointment_id=appointment_id,
            consultation_fee=consultation_fee,
            additional_charges=additional_charges,
            total_amount=total_amount,
            payment_status=payment_status,
            payment_mode=payment_mode,
            is_active=True
        )

        db.add(billing)

        # ----------------------------------------------------
        # Update appointment status
        # ----------------------------------------------------

        if appointment is not None:
            appointment.status = "completed"

        # Save everything together
        db.commit()

        db.refresh(billing)

        return billing

    except Exception:

        # If anything fails, undo everything
        db.rollback()

        raise HTTPException(
            status_code=500,
            detail="Billing creation failed. Transaction rolled back."
        )