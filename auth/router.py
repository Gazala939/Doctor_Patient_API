from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from passlib.context import CryptContext

from db import get_db
from models.user import User
from schemas.user import UserCreate, UserLogin
from auth.jwt import create_access_token, verify_token


pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


# Register
@router.post(
    "/register",
    summary="Register a new user",
    description="Creates a new user account with a hashed password and assigned role.",
    responses={
        200: {
            "description": "User registered successfully"
        },
        400: {
            "description": "Email already registered"
        }
    }
)
def register(
    user: UserCreate,
    db: Session = Depends(get_db)
):
    existing_user = db.query(User).filter(
        User.email == user.email
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    new_user = User(
        username=user.name,
        email=user.email,
        password=pwd_context.hash(user.password),
        role=user.role
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "message": "User registered successfully",
        "user_id": new_user.id
    }


# Login
@router.post(
    "/login",
    summary="Login user",
    description="Authenticates a user and returns a JWT access token.",
    responses={
        200: {
            "description": "Login successful"
        },
        401: {
            "description": "Invalid email or password"
        }
    }
)
def login(
    user: UserLogin,
    db: Session = Depends(get_db)
):
    existing_user = db.query(User).filter(
        User.email == user.email
    ).first()

    if not existing_user:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    if not pwd_context.verify(
        user.password,
        existing_user.password
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    token = create_access_token({
        "user_id": existing_user.id,
        "role": existing_user.role
    })

    return {
        "message": "Login successful",
        "access_token": token,
        "token_type": "bearer"
    }


# Protected route
@router.get(
    "/protected",
    summary="Check authentication",
    description="Returns information about the currently authenticated user.",
    responses={
        200: {
            "description": "User is authenticated"
        },
        401: {
            "description": "Authentication required"
        }
    }
)
def protected_route(
    payload: dict = Depends(verify_token)
):
    return {
        "message": "You are authenticated",
        "user_id": payload["user_id"],
        "role": payload["role"]
    }