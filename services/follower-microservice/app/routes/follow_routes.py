from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.auth.auth import get_current_user_id
from app.schemas.follower_schemas import (
    FollowResponse,
    FollowersIdsResponse,
    FollowingIdsResponse
)
from app.services import follower_service

router = APIRouter(prefix="/follow", tags=["Follow"])


@router.post(
    "/{user_id}",
    response_model=FollowResponse,
    status_code=status.HTTP_201_CREATED
)
def follow(
    user_id: int,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id)
):
    return follower_service.follow_user(db, current_user_id, user_id)


@router.delete(
    "/{user_id}",
    response_model=FollowResponse
)
def unfollow(
    user_id: int,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id)
):
    return follower_service.unfollow_user(db, current_user_id, user_id)


@router.get(
    "/{user_id}/followers",
    response_model=FollowersIdsResponse
)
def get_followers(
    user_id: int,
    db: Session = Depends(get_db),
    # current_user_id: int = Depends(get_current_user_id)
):
    return follower_service.get_followers(db, user_id)


@router.get(
    "/{user_id}/following",
    response_model=FollowingIdsResponse
)
def get_following(
    user_id: int,
    db: Session = Depends(get_db),
    # current_user_id: int = Depends(get_current_user_id)
):
    return follower_service.get_following(db, user_id)