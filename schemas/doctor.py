from typing import Optional

from pydantic import BaseModel, EmailStr


class DoctorCreate(BaseModel):

    name: str
    specialization: str
    email: EmailStr
    user_id: int

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Dr. Ahmed Khan",
                "specialization": "Cardiologist",
                "email": "ahmed@example.com",
                "user_id": 2
            }
        }


class DoctorUpdate(BaseModel):

    name: str
    specialization: str
    email: EmailStr

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Dr. Ahmed Khan",
                "specialization": "Cardiologist",
                "email": "ahmed@example.com"
            }
        }


class DoctorPatch(BaseModel):

    name: Optional[str] = None
    specialization: Optional[str] = None
    email: Optional[EmailStr] = None

    class Config:
        json_schema_extra = {
            "example": {
                "specialization": "Neurologist"
            }
        }