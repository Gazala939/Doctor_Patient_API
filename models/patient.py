from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship

from db import Base


class Patient(Base):
    __tablename__ = "patients"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    name = Column(
        String(100),
        nullable=False
    )

    age = Column(
        Integer,
        nullable=False
    )

    phone = Column(
        String(15),
        nullable=False
    )

    is_active = Column(
        Boolean,
        default=True
    )

    doctor_id = Column(
        Integer,
        ForeignKey("doctors.id"),
        nullable=True
    )

    # Relationship with Doctor
    doctor = relationship(
        "Doctor",
        back_populates="patients"
    )