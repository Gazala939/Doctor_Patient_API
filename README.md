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