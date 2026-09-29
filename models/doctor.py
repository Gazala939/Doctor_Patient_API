from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from db import Base


class Doctor(Base):
    __tablename__ = "doctors"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        unique=True,
        nullable=True
    )

    name = Column(
        String(100),
        nullable=False
    )

    specialization = Column(
        String(100),
        nullable=False
    )

    email = Column(
        String(100),
        unique=True,
        nullable=False,
        index=True
    )

    is_active = Column(
        Boolean,
        default=True
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

    # Relationship with User
    user = relationship("User")

    # Relationship with Patient
    patients = relationship(
        "Patient",
        back_populates="doctor"
    )
    
    appointments = relationship(
        "Appointment",
        back_populates="doctor"
    )