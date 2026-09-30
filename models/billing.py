from sqlalchemy import Column, Integer, ForeignKey, Float, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

from db import Base


class Billing(Base):
    __tablename__ = "billings"

    id = Column(Integer, primary_key=True, index=True)

    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)

    doctor_id = Column(Integer, ForeignKey("doctors.id"), nullable=False)

    appointment_id = Column(
        Integer,
        ForeignKey("appointments.id"),
        nullable=True,
        unique=True
    )

    consultation_fee = Column(Float, nullable=False)

    additional_charges = Column(Float, default=0)

    total_amount = Column(Float, nullable=False)

    payment_status = Column(
        String,
        default="pending",
        nullable=False
    )

    payment_mode = Column(
        String,
        nullable=True
    )

    is_active = Column(Boolean, default=True)

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    patient = relationship(
        "Patient",
        back_populates="billings"
    )

    doctor = relationship(
        "Doctor",
        back_populates="billings"
    )

    appointment = relationship(
        "Appointment",
        back_populates="billing"
    )