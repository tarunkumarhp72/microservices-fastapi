
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.auth.auth import get_current_user        
from app.models.user_model import User
from app.schemas.user_schema import FollowResponse, FollowersListResponse, FollowingListResponse
from app.services import follower_service

router = APIRouter(prefix="/users", tags=["Follow"])


@router.post(
    "/{user_id}/follow",
    response_model=FollowResponse,
    status_code=status.HTTP_201_CREATED,
)
def follow(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Follow a user.
    Requires: Bearer JWT token in Authorization header.
    """
    result = follower_service.follow_user(db, current_user.id, user_id)
    return result


@router.delete(
    "/{user_id}/unfollow",
    response_model=FollowResponse,
    status_code=status.HTTP_200_OK,
)
def unfollow(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Unfollow a user.
    Requires: Bearer JWT token in Authorization header.
    """
    result = follower_service.unfollow_user(db, current_user.id, user_id)
    return result


@router.get(
    "/{user_id}/followers",
    response_model=FollowersListResponse,
)
def followers(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Get all followers of a user.
    (Public within the app — any logged-in user can view.)
    """
    return follower_service.get_followers(db, user_id)


@router.get(
    "/{user_id}/following",
    response_model=FollowingListResponse,
)
def following(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Get all users that a given user follows.
    """
    return follower_service.get_following(db, user_id)


@router.get("/following-ids/{user_id}")
def following_ids(
    user_id: int,
    db: Session = Depends(get_db)
):
    return follower_service.get_following_ids(
        db,
        user_id
    )