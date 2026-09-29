import os
from dotenv import load_dotenv
from datetime import datetime, timedelta, timezone
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(
    os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30")
)

security = HTTPBearer()

def create_access_token(data: dict):

    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(
    minutes=ACCESS_TOKEN_EXPIRE_MINUTES
)

    to_encode.update({
        "exp": expire
    })

    token = jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return token

def verify_token(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):

    token = credentials.credentials

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        return payload

    except Exception:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )
        
def require_role(required_role: str):

    def role_checker(
        payload: dict = Depends(verify_token)
    ):

        if payload.get("role") != required_role:
            raise HTTPException(
                status_code=403,
                detail="Forbidden"
            )

        return payload

    return role_checker