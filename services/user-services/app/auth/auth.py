from fastapi import Depends
from fastapi import HTTPException
from fastapi.security import HTTPBearer
from requests import Session
from app.core.security import decode_access_token
from app.database import get_db
from app.models.user_model import User

security = HTTPBearer()

def get_current_user(
    credentials=Depends(security),
     db: Session = Depends(get_db)  
):
    token = credentials.credentials

    payload = decode_access_token(token)

    if not payload:
        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )

    user_id = payload.get("sub")   # ← get id from payload

    user = db.query(User).filter(User.id == int(user_id)).first()  # ← fetch User

    if not user:
        raise HTTPException(
            status_code=401,
            detail="User not found"
        )

    return user 