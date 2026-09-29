from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):

    name: str
    email: EmailStr
    password: str
    role: str

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Admin User",
                "email": "admin@example.com",
                "password": "Admin@123",
                "role": "Admin"
            }
        }


class UserLogin(BaseModel):

    email: EmailStr
    password: str

    class Config:
        json_schema_extra = {
            "example": {
                "email": "admin@example.com",
                "password": "Admin@123"
            }
        }