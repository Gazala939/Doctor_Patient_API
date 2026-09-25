from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship

from db import Base


class Doctor(Base):
    __tablename__ = "doctors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    specialization = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False, index=True)
    is_active = Column(Boolean, default=True)

    patients = relationship(
        "Patient",
        back_populates="doctor"
    )