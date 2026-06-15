from datetime import datetime, timezone

from fastapi import APIRouter
from fastapi import Depends, HTTPException

from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session

from app.database import get_db

from app.schemas.user_schema import UserCreate, LoginRequest
from app.schemas.user_schema import UserResponse

from app.services.user_service import create_user, login_user
from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token,
    decode_token,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    REFRESH_TOKEN_EXPIRE_DAYS
)
from app.auth.auth import get_current_user
from app.cache.redis_client import redis_client


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

security=HTTPBearer()

@router.post(
    "/register",
    response_model=UserResponse
)
def register_user(
    user: UserCreate,
    db: Session = Depends(get_db)
):
    return create_user(
        user,
        db
    )


@router.post("/login")
def login(
    user: LoginRequest,
    db: Session = Depends(get_db)
):
    result = login_user(user, db)

    if not result:
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )
    user_obj=result

    new_access_token=create_access_token(data={"sub":str(user_obj.id)})
    new_refresh_token=create_refresh_token(data={"sub":str(user_obj.id)})
    

    redis_client.setex(f"refresh_token:{user_obj.id}",REFRESH_TOKEN_EXPIRE_DAYS*24*60*60,new_refresh_token)
    return {
        "access_token": new_access_token,
        "refresh_token": new_refresh_token,
        "token_type": "bearer"
    }

@router.post("/logout")
def logout(
    credentials=Depends(security),
    current_user=Depends(get_current_user)
):
    token = credentials.credentials
    payload = decode_token(token)

    if payload:
        exp = payload.get("exp")  # expiry timestamp from token
        
        if exp:
            now = int(datetime.now(timezone.utc).timestamp())
            remaining_seconds = exp - now  # how many seconds left

            if remaining_seconds > 0:
                redis_client.setex(
                    f"blacklist:{token}",
                    remaining_seconds,
                    "blacklisted"
                )

    redis_client.delete(f"refresh_token:{current_user.id}")

    return {"message": "Logged out successfully"}

        
        
    
 


@router.get("/profile")
def profile(
    current_user=Depends(get_current_user)
):
    return {
        "message": "Profile Access Granted",
        "user": current_user
    }