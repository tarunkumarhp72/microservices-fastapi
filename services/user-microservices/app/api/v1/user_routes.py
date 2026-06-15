

from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.user_schema import UserCreate, LoginRequest, UserResponse
from app.services.user_service import create_user, login_user
from shared.exceptions import UnauthorizedException
from shared.security import decode_token
from app.auth.auth import get_current_user, create_access_token, create_refresh_token, REFRESH_TOKEN_EXPIRE_DAYS
   

from app.auth.auth import get_current_user
from shared.redis_client import redis_client

# ── Shared lib imports ──────────────────────────────────────────────
from shared.rate_limit import strict_limiter, standard_limiter
from shared.logger import get_logger

logger = get_logger("user-service")

router = APIRouter(prefix="/users", tags=["Users"])
security = HTTPBearer()


# ─────────────────────────────────────────────
# Register — Strict rate limit (10/min)
# ─────────────────────────────────────────────
@router.post(
    "/register",
    response_model=UserResponse,
    dependencies=[Depends(strict_limiter)]  # ← 10 req/min per IP
)
def register_user(
    request: Request,
    user: UserCreate,
    db: Session = Depends(get_db)
):
    request_id = getattr(request.state, "request_id", "unknown")
    logger.info(
        "Register attempt",
        extra={"request_id": request_id, "email": user.email}
    )
    result = create_user(user, db)
    logger.info(
        "User registered successfully",
        extra={"request_id": request_id, "user_id": result.id}
    )
    return result


# ─────────────────────────────────────────────
# Login — Strict rate limit (10/min)

# ─────────────────────────────────────────────
@router.post(
    "/login",
    dependencies=[Depends(strict_limiter)]  # ← 10 req/min per IP
)
def login(
    request: Request,
    user: LoginRequest,
    db: Session = Depends(get_db)
):
    request_id = getattr(request.state, "request_id", "unknown")
    logger.info(
        "Login attempt",
        extra={"request_id": request_id, "email": user.email}
    )

    result = login_user(user, db)
    if not result:
        logger.warning(
            "Login failed — invalid credentials",
            extra={"request_id": request_id, "email": user.email}
        )
        raise UnauthorizedException("Invalid email or password")

    user_obj = result
    new_access_token = create_access_token(data={"sub": str(user_obj.id)})
    new_refresh_token = create_refresh_token(data={"sub": str(user_obj.id)})

    redis_client.setex(
        f"refresh_token:{user_obj.id}",
        REFRESH_TOKEN_EXPIRE_DAYS * 24 * 60 * 60,
        new_refresh_token
    )

    logger.info(
        "Login successful",
        extra={"request_id": request_id, "user_id": user_obj.id}
    )

    return {
        "access_token": new_access_token,
        "refresh_token": new_refresh_token,
        "token_type": "bearer"
    }


# ─────────────────────────────────────────────
# Logout — Standard rate limit
# ─────────────────────────────────────────────
@router.post(
    "/logout",
    dependencies=[Depends(standard_limiter)]
)
def logout(
    request: Request,
    credentials=Depends(security),
    current_user=Depends(get_current_user)
):
    token = credentials.credentials
    payload = decode_token(token)
    request_id = getattr(request.state, "request_id", "unknown")

    if payload:
        exp = payload.get("exp")
        if exp:
            now = int(datetime.now(timezone.utc).timestamp())
            remaining_seconds = exp - now
            if remaining_seconds > 0:
                redis_client.setex(f"blacklist:{token}", remaining_seconds, "blacklisted")

    redis_client.delete(f"refresh_token:{current_user.id}")

    logger.info(
        "User logged out",
        extra={"request_id": request_id, "user_id": current_user.id}
    )
    return {"message": "Logged out successfully"}


# ─────────────────────────────────────────────
# Profile — Standard rate limit
# ─────────────────────────────────────────────
@router.get(
    "/profile",
    dependencies=[Depends(standard_limiter)]
)
def profile(
    request: Request,
    current_user=Depends(get_current_user)
):
    return {
        "message": "Profile Access Granted",
        "user": current_user
    }