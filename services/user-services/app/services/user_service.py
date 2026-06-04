from sqlalchemy.orm import Session

from app.models.user_model import User
from app.schemas.user_schema import UserCreate
from app.core.security import hash_password
from app.core.security import (
    verify_password,
    create_access_token
)


def create_user(user_data, db):
    hashed_password = hash_password(user_data.password)

    user = User(
        username=user_data.username,
        email=user_data.email,
        password=hashed_password
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


def login_user(login_data, db):
    user = (
        db.query(User)
        .filter(User.email == login_data.email)
        .first()
    )

    if not user:
        return None

    if not verify_password(
        login_data.password,
        user.password
    ):
        return None

    token = create_access_token(
        {"sub": str(user.id)}
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }