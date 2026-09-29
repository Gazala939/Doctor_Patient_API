from sqlalchemy import Column, Integer, DateTime, String, ForeignKey
from sqlalchemy.orm import relationship

from db import Base


class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    doctor_id = Column(
        Integer,
        ForeignKey("doctors.id"),
        nullable=False,
        index=True
    )

    patient_id = Column(
        Integer,
        ForeignKey("patients.id"),
        nullable=False,
        index=True
    )

    appointment_date = Column(
        DateTime,
        nullable=False,
        index=True
    )

    status = Column(
        String,
        default="scheduled",
        nullable=False
    )

    created_at = Column(
        DateTime,
        nullable=False
    )

    updated_at = Column(
        DateTime,
        nullable=False
    )

    created_by = Column(
        Integer,
        nullable=True
    )

    updated_by = Column(
        Integer,
        nullable=True
    )

    doctor = relationship(
        "Doctor",
        back_populates="appointments"
    )

    patient = relationship(
        "Patient",
        back_populates="appointments"
    )