# Doctor Patient Management API

## Project Overview

Doctor Patient Management API is a backend application built using FastAPI for managing doctors, patients, doctor-patient assignments, appointments, authentication, and authorization.

The project uses --JWT authentication--, --role-based authorization--, --SQLAlchemy--, and --SQLite-- for database persistence.

# Technologies Used

    * Python
    * FastAPI
    * Uvicorn
    * SQLAlchemy
    * SQLite
    * Pydantic
    * JWT Authentication
    * Python-Jose
    * Passlib / Bcrypt
    * Pytest
    * Pytest-Cov

## Main Features

    * User registration and login
    * JWT-based authentication
    * Role-based authorization
    * Admin and Doctor roles
    * Doctor management
    * Patient management
    * Doctor-patient assignment
    * Appointment management
    * Appointment conflict prevention
    * Soft delete
    * Pagination
    * Input validation
    * Database constraints
    * Audit tracking
    * Global exception handling
    * Uniform error responses
    * Basic rate limiting
    * API response-time measurement
    * Unit and API testing
    * Swagger/OpenAPI documentation

## User Roles

### Admin

Admin users can:

    * Manage doctors
    * Manage patients
    * Manage appointments
    * Perform authorized create, update, patch, and delete operations

### Doctor

Doctor users can:

    * View doctors
    * View assigned patients
    * View related authorized information
    * View appointments according to authorization rules

Doctors cannot perform Admin-only management operations.



## Installation

Clone or copy the project and open the project directory:

    ```bash
    cd C:\Doctor_Patient_API
    ```

Create a virtual environment:

    ```bash
    python -m venv .venv
    ```

Activate the virtual environment on Windows:

    ```bash
    .venv\Scripts\activate
    ```

Install the required packages:

    ```bash
    pip install -r requirements.txt
    ```

## Environment Variables

Create a `.env` file in the project root.


Do not upload real secrets or passwords to GitHub.

## Database

The application uses **SQLite** with SQLAlchemy.

Database:

    ```text
    doctor_patient.db
    ```

Foreign key support is enabled in SQLite.

Database tables include:

    * Users
    * Doctors
    * Patients
    * Appointments

## Running the Application

Start the FastAPI application using:

    ```bash
    python -m uvicorn index:app --reload
    ```

The application will be available at:

http://127.0.0.1:8000


## Swagger Documentation

Interactive API documentation is available at:


http://127.0.0.1:8000/docs


OpenAPI JSON:


http://127.0.0.1:8000/openapi.json

Swagger can be used to test the API endpoints and JWT authentication.

## Authentication Flow

### 1. Register

POST /auth/register


Create an Admin or Doctor user.

### 2. Login

POST /auth/login


Login using registered credentials.

The API returns a JWT access token.

# 3. Authorize

Use the JWT token in Swagger's **Authorize** button to access protected endpoints.

## Main API Modules

### Authentication

POST /auth/register
POST /auth/login


### Doctors

Doctor APIs support:

    * Create doctor
    * Get doctors
    * Get doctor by ID
    * Update doctor
    * Patch doctor
    * Soft delete doctor
    * View patients assigned to a doctor
    * View doctor appointments

### Patients

Patient APIs support:

    * Create patient
    * Get patients
    * Get patient by ID
    * Update patient
    * Patch patient
    * Soft delete patient
    * Doctor assignment
    * Patient appointment access

### Appointments

Appointment APIs support:

    * Create appointment
    * Get appointments
    * Get appointment by ID
    * Update appointment
    * Delete appointment
    * Get appointments for a doctor
    * Get appointments for a patient

## Validation

The application validates incoming data using Pydantic.

Examples include:

    * Valid email format
    * Patient age must be greater than zero
    * Phone number validation
    * Required fields
    * Valid doctor and patient IDs
    * Active doctor validation
    * Appointment status validation

## Appointment Conflict Prevention

The API checks for conflicting appointments for the same doctor before creating or updating an appointment.

This helps prevent overlapping appointments.

## Soft Delete

Doctors and patients use soft deletion.

Instead of permanently removing the database record:

```text
is_active = False
```

is used to mark the record inactive.

## Audit Tracking

The application records:

    * `created_at`
    * `updated_at`
    * `created_by`
    * `updated_by`

JWT user information is used to identify the user performing authorized operations.

## Error Handling

The application includes:

    * Global HTTP exception handling
    * Validation error handling
    * Database exception handling
    * Consistent error responses
    * Meaningful HTTP status codes

Common responses include:

400 Bad Request
401 Unauthorized
403 Forbidden
404 Not Found
422 Validation Error


## Performance

The project includes:

    * Database indexes
    * Pagination for list APIs
    * Optimized SQLAlchemy queries
    * Avoidance of unnecessary database queries
    * Response-time measurement

## Rate Limiting

Basic rate limiting is implemented to help protect the API from excessive requests.

## Testing

The project uses **Pytest** and **Pytest-Cov**.

Run all tests:


python -m pytest


Run tests with coverage:

python -m pytest --cov=. --cov-report=term-missing


### Test Result

text 60 passes 82% coverage
 
The project exceeds the required minimum test coverage of --70%--.

The screenshots demonstrate:

    * Swagger overview
    * User registration
    * Login and JWT authentication
    * Swagger authorization
    * Doctor APIs
    * Patient APIs
    * Appointment APIs
    * Role-based authorization
    * Validation errors
    * Swagger documentation

## Billing

The Billing module manages patient billing and payment information.

Billing APIs support:

    * Create billing
    * Get billing by ID
    * Get all billings
    * Get billings for a patient
    * Get billings for a doctor
    * Update billing using PUT
    * Partial update using PATCH
    * Soft delete billing
    * Billing filters
    * Pagination
    * Revenue reports

### Billing Fields

Each billing record contains:

    * Patient ID
    * Doctor ID
    * Appointment ID
    * Consultation fee
    * Additional charges
    * Total amount
    * Payment status
    * Payment mode
    * Active status
    * Created and updated timestamps

### Billing Validation

The API validates:

    * Patient must exist and be active
    * Doctor must exist and be active
    * Appointment must belong to the selected doctor and patient
    * Billing cannot be created for a cancelled appointment
    * Duplicate billing for the same appointment is prevented
    * Total amount is calculated automatically

### Payment Status

Supported payment statuses:

    * pending
    * paid
    * cancelled

Supported payment modes:

    * cash
    * card
    * upi

### Billing Authorization

Admin users can:

    * Create billing
    * View billing
    * Update billing
    * Patch billing
    * Delete billing

Doctor users can:

    * View billings related to their patients

Doctors cannot delete billing records.

### Revenue Reports

The API provides revenue reports including:

    * Total revenue
    * Revenue per doctor
    * Revenue per day

Example:

GET /reports/revenue

The revenue report supports filtering by:

    * Doctor ID
    * From date
    * To date

### Billing Soft Delete

Billing records are soft deleted using:

is_active = False