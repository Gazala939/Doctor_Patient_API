from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field


class AppointmentStatus(str, Enum):
    scheduled = "scheduled"
    completed = "completed"
    cancelled = "cancelled"


class AppointmentCreate(BaseModel):
    doctor_id: int = Field(gt=0)
    patient_id: int = Field(gt=0)
    appointment_date: datetime
    status: AppointmentStatus = AppointmentStatus.scheduled

    class Config:
        json_schema_extra = {
            "example": {
                "doctor_id": 1,
                "patient_id": 1,
                "appointment_date": "2026-10-01T10:00:00",
                "status": "scheduled"
            }
        }


class AppointmentUpdate(BaseModel):
    doctor_id: int = Field(gt=0)
    patient_id: int = Field(gt=0)
    appointment_date: datetime
    status: AppointmentStatus

    class Config:
        json_schema_extra = {
            "example": {
                "doctor_id": 1,
                "patient_id": 1,
                "appointment_date": "2026-10-01T11:00:00",
                "status": "completed"
            }
        }


class AppointmentResponse(BaseModel):
    id: int
    doctor_id: int
    patient_id: int
    appointment_date: datetime
    status: AppointmentStatus

    class Config:
        from_attributes = True