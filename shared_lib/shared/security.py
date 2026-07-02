from fastapi import HTTPException
import os
from fastapi import Header
from jose import jwt, JWTError
from dotenv import load_dotenv
load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
INTERNAL_SERVICE_TOKEN = os.getenv("INTERNAL_SERVICE_TOKEN", "")


if not SECRET_KEY:
    raise RuntimeError("SECRET_KEY is not set")


def decode_token(token: str):
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )
        return payload
    except JWTError:
        return None
    
INTERNAL_SERVICE_TOKEN = os.getenv("INTERNAL_SERVICE_TOKEN", "")


def verify_internal_token(x_internal_token: str = Header(None)):
    if x_internal_token != INTERNAL_SERVICE_TOKEN:
        raise HTTPException(
            status_code=403,
            detail="Internal access only"
        )