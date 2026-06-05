from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer
from app.core.security import decode_token

security = HTTPBearer()


def get_current_user_id(credentials=Depends(security)) -> int:
    token = credentials.credentials
    payload = decode_token(token)

    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")

    if payload.get("type") != "access":
        raise HTTPException(status_code=401, detail="Invalid token type")

    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid token payload")

    return int(user_id)