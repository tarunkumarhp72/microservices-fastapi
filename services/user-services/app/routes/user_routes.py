from fastapi import APIRouter
from fastapi import Depends, HTTPException

from sqlalchemy.orm import Session

from app.database import get_db

from app.schemas.user_schema import UserCreate, LoginRequest
from app.schemas.user_schema import UserResponse

from app.services.user_service import create_user, login_user
from app.core.security import (
    hash_password,
    verify_password,
    create_access_token
)
from app.auth.auth import get_current_user


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


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

    return result




@router.get("/profile")
def profile(
    current_user=Depends(get_current_user)
):
    return {
        "message": "Profile Access Granted",
        "user": current_user
    }