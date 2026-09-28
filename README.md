Doctor Patient API

Technologies Used
- Python
- FastAPI
- Pydantic
- SQLAlchemy
- SQLite
- JWT Authentication
- Uvicorn
- Passlib / bcrypt
- python-dotenv
- Swagger UI

Authentication
- User registration
- User login
- JWT-based authentication
- Protected APIs
- Role-based authorization

Admin can:
- Create doctors
- View doctors
- Update doctors
- Soft delete doctors
- Create patients
- View all patients
- Assign patients to doctors

Doctor can:
- View their assigned patients
- View individual patients - assigned to them



The application validates:
- Unique doctor email
- Valid email format
- Patient age must be greater than 0
- Patient phone must contain only digits
- Patient phone must contain 10–15 digits
- Required authentication for protected APIs
- Role-based access to protected resources

Environment Configuration
Create a .env file in the project root:

SECRET_KEY=my_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

How to Run the Project
1. python -m venv venv
2. Activate:
.\venv\Scripts\activate
3. pip install fastapi uvicorn sqlalchemy pydantic python-dotenv python-jose[cryptography] passlib[bcrypt] email-validator
4. Start the server

Follow up to fat api:
User Authentication:
  User registration
  User login
  Password hashing
  JWT token generation
  Protected API endpoints
  Role-based authorization

Doctor Management:
    Create doctor
    Get doctor by ID
    Get all doctors
    Update doctor
    Partially update doctor
    Soft delete/deactivate doctor
    Doctor email uniqueness validation
    Filter doctors by specialization
    Filter doctors by active status
    Pagination

Patient Management:
    Create patient
    Get patient by ID
    Get all patients
    Update patient
    Partially update patient
    Soft delete/deactivate patient
    Patient age validation
    Patient phone number validation
    Filter patients by age
    Pagination

Doctor–Patient Relationship:
    Assign a patient to a doctor
    Prevent assignment to inactive doctors
    Get all patients assigned to a doctor
    Doctors can view only their assigned patients