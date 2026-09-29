from typing import Optional
from pydantic import BaseModel, field_validator


class PatientCreate(BaseModel):
    name: str
    age: int
    phone: str
    doctor_id: int

    @field_validator("age")
    @classmethod
    def validate_age(cls, value):
        if value <= 0:
            raise ValueError("Age must be greater than 0")
        return value

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, value):

        if not value.isdigit():
            raise ValueError("Phone must contain only digits")

        if len(value) != 10:
            raise ValueError("Phone must be exactly 10 digits")

        return value

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Rahul Sharma",
                "age": 35,
                "phone": "9876543210",
                "doctor_id": 1
            }
        }


class PatientUpdate(BaseModel):
    name: str
    age: int
    phone: str
    doctor_id: int

    @field_validator("age")
    @classmethod
    def validate_age(cls, value):
        if value <= 0:
            raise ValueError("Age must be greater than 0")
        return value

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, value):

        if not value.isdigit():
            raise ValueError("Phone must contain only digits")

        if len(value) != 10:
            raise ValueError("Phone must be exactly 10 digits")

        return value

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Rahul Sharma",
                "age": 36,
                "phone": "9876543210",
                "doctor_id": 1
            }
        }


class PatientPatch(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    phone: Optional[str] = None
    doctor_id: Optional[int] = None

    @field_validator("age")
    @classmethod
    def validate_age(cls, value):

        if value is not None and value <= 0:
            raise ValueError("Age must be greater than 0")

        return value

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, value):

        if value is not None:

            if not value.isdigit():
                raise ValueError("Phone must contain only digits")

            if len(value) != 10:
                raise ValueError("Phone must be exactly 10 digits")

        return value

    class Config:
        json_schema_extra = {
            "example": {
                "age": 36
            }
        }