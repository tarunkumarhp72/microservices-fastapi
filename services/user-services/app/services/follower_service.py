# user_service/follower_service.py

from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.user_model import Follower, User


def follow_user(db: Session, current_user_id: int, target_user_id: int) -> dict:
    """
    current_user follows target_user.
    Raises 400 if already following or trying to follow yourself.
    """
    # Cannot follow yourself
    if current_user_id == target_user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You cannot follow yourself.",
        )

    # Target user must exist
    target = db.query(User).filter(User.id == target_user_id).first()
    if not target:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User {target_user_id} not found.",
        )

    # Check for existing follow
    existing = (
        db.query(Follower)
        .filter(
            Follower.follower_id == current_user_id,
            Follower.followed_id == target_user_id,
        )
        .first()
    )
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"You are already following user {target_user_id}.",
        )

    new_follow = Follower(follower_id=current_user_id, followed_id=target_user_id)
    db.add(new_follow)
    db.commit()

    return {"message": f"You are now following {target.username}."}


def unfollow_user(db: Session, current_user_id: int, target_user_id: int) -> dict:
    """
    current_user unfollows target_user.
    Raises 404 if the follow relationship doesn't exist.
    """
    if current_user_id == target_user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You cannot unfollow yourself.",
        )

    follow = (
        db.query(Follower)
        .filter(
            Follower.follower_id == current_user_id,
            Follower.followed_id == target_user_id,
        )
        .first()
    )
    if not follow:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="You are not following this user.",
        )

    db.delete(follow)
    db.commit()

    return {"message": "Unfollowed successfully."}


def get_followers(db: Session, user_id: int) -> dict:
    """Returns all users who follow user_id."""
    # Confirm user exists
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")

    rows = db.query(Follower).filter(Follower.followed_id == user_id).all()

    follower_ids = [row.follower_id for row in rows]
    users = db.query(User).filter(User.id.in_(follower_ids)).all()

    return {"total": len(users), "users": users}


def get_following(db: Session, user_id: int) -> dict:
    """Returns all users that user_id follows."""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")

    rows = db.query(Follower).filter(Follower.follower_id == user_id).all()

    followed_ids = [row.followed_id for row in rows]
    users = db.query(User).filter(User.id.in_(followed_ids)).all()

    return {"total": len(users), "users": users}


def get_following_ids(
    db: Session,
    user_id: int
):
    rows = (
        db.query(Follower)
        .filter(Follower.follower_id == user_id)
        .all()
    )

    return [row.followed_id for row in rows]