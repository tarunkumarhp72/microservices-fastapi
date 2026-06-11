from sqlalchemy.orm import Session
from app.models.user_model import User
from app.schemas.user_schema import UserCreate
from app.core.security import hash_password, verify_password


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

    if not verify_password(login_data.password, user.password):
        return None

    return user