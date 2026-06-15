from fastapi import Depends
from fastapi import HTTPException
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session
from app.core.security import decode_token
from app.database import get_db
from app.models.user_model import User
from app.cache.redis_client import redis_client

security = HTTPBearer()

def get_current_user(
    credentials=Depends(security),
     db: Session = Depends(get_db)  
):
    token = credentials.credentials

    payload = decode_token(token)

    if not payload:
        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )
    if payload.get("type") != "access":
        raise HTTPException(
            status_code=401,
            detail="Invalid token type"
        )
    
    is_blacklisted=redis_client.get(f"blacklisted:{token}")
    if is_blacklisted:
        raise HTTPException(
            status_code=401,
            detail="Token has been revoked"
        )
    user_id = payload.get("sub")   

    user = db.query(User).filter(User.id == int(user_id)).first() 

    if not user:
        raise HTTPException(
            status_code=401,
            detail="User not found"
        )

    return user 