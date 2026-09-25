from pydantic import BaseModel, EmailStr


class DoctorCreate(BaseModel):
    name: str
    specialization: str
    email: EmailStr


class DoctorUpdate(BaseModel):
    name: str
    specialization: str
    email: EmailStr