from pydantic import BaseModel, field_validator


class PatientCreate(BaseModel):
    name: str
    age: int
    phone: str

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

        if not 10 <= len(value) <= 15:
            raise ValueError("Phone must be 10 to 15 digits")

        return value