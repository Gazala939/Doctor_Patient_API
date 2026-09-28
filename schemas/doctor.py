from typing import Optional
from pydantic import BaseModel, EmailStr


class DoctorCreate(BaseModel):
    name: str
    specialization: str
    email: EmailStr
    user_id: int


class DoctorUpdate(BaseModel):
    name: str
    specialization: str
    email: EmailStr


class DoctorPatch(BaseModel):
    name: Optional[str] = None
    specialization: Optional[str] = None
    email: Optional[EmailStr] = None