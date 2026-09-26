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