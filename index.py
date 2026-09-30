from fastapi import FastAPI, Request, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from db import Base, engine

# Import models
from models.user import User
from models.doctor import Doctor
from models.patient import Patient
from models.billing import Billing
from models.appointment import Appointment

from auth.router import router as auth_router
from doctors.router import router as doctor_router
from patients.router import router as patient_router
from appointments.router import router as appointment_router
from billings.router import router as billing_router

import time

from collections import defaultdict
from datetime import datetime, timedelta

Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Doctor Patient Management API",
    description="""
## Doctor Patient Management API

Backend API for managing:

- User authentication
- Role-based authorization
- Doctors
- Patients
- Doctor-Patient assignments
- Appointments
- Audit information

### Authentication

JWT authentication is used to protect the API.

### Roles

**Admin**
- Manage doctors
- Manage patients
- Manage appointments

**Doctor**
- View assigned patients
- View related information based on authorization

### API Features

- JWT authentication
- Role-based authorization
- CRUD operations
- Soft delete
- Pagination
- Data validation
- Appointment conflict prevention
- Audit tracking
- Global error handling
- Rate limiting
""",
    version="1.0.0"
)

request_records = defaultdict(list)

RATE_LIMIT = 100
RATE_WINDOW = timedelta(minutes=1)

@app.exception_handler(HTTPException)
async def http_exception_handler(
    request: Request,
    exc: HTTPException
):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "error": exc.detail
        }
    )
    
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError
):
    errors = []

    for error in exc.errors():
        errors.append({
            "field": ".".join(
                str(location) for location in error["loc"]
            ),
            "message": error["msg"]
        })

    return JSONResponse(
        status_code=422,
        content={
            "success": False,
            "error": "Validation error",
            "details": errors
        }
    )

# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(
    request: Request,
    exc: Exception
):
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": "Internal Server Error",
            "message": "Something went wrong on the server"
        }
    )

@app.middleware("http")
async def rate_limit_middleware(request: Request, call_next):

    client_ip = request.client.host

    current_time = datetime.utcnow()

    request_records[client_ip] = [
        request_time
        for request_time in request_records[client_ip]
        if current_time - request_time < RATE_WINDOW
    ]

    if len(request_records[client_ip]) >= RATE_LIMIT:
        return JSONResponse(
            status_code=429,
            content={
                "success": False,
                "error": "Too many requests",
                "message": "Rate limit exceeded. Please try again later."
            }
        )

    request_records[client_ip].append(current_time)
    response = await call_next(request)
    return response

@app.middleware("http")
async def measure_response_time(request, call_next):

    start_time = time.time()
    response = await call_next(request)
    end_time = time.time()
    response_time = end_time - start_time
    response.headers["X-Response-Time"] = (
        f"{response_time:.4f} seconds"
    )
    return response


app.include_router(auth_router)
app.include_router(doctor_router)
app.include_router(patient_router)
app.include_router(appointment_router)
app.include_router(billing_router)


@app.get("/")
def home():
    return {
        "message": "Doctor Patient API is running"
    }