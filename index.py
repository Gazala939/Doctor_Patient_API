from fastapi import FastAPI

from db import create_tables

from models.user import User
from models.doctor import Doctor
from models.patient import Patient

from auth.router import router as auth_router
from doctors.router import router as doctor_router
from patients.router import router as patient_router


create_tables()


app = FastAPI(
    title="Doctor Patient API",
    description="Backend API for Doctor and Patient Management",
    version="1.0.0"
)


app.include_router(auth_router)
app.include_router(doctor_router)
app.include_router(patient_router)


@app.get("/")
def home():
    return {
        "message": "Doctor Patient API is running"
    }