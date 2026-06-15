from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.follower_model import Follow


def follow_user(db: Session, follower_id: int, followed_id: int) -> dict:
    if follower_id == followed_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You cannot follow yourself"
        )

    existing = db.query(Follow).filter(
        Follow.follower_id == follower_id,
        Follow.followed_id == followed_id
    ).first()

    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You are already following this user"
        )

    new_follow = Follow(
        follower_id=follower_id,
        followed_id=followed_id
    )
    db.add(new_follow)
    db.commit()

    return {"message": f"You are now following user {followed_id}"}


def unfollow_user(db: Session, follower_id: int, followed_id: int) -> dict:
    if follower_id == followed_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You cannot unfollow yourself"
        )

    follow = db.query(Follow).filter(
        Follow.follower_id == follower_id,
        Follow.followed_id == followed_id
    ).first()

    if not follow:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="You are not following this user"
        )

    db.delete(follow)
    db.commit()

    return {"message": f"Unfollowed user {followed_id} successfully"}


def get_followers(db: Session, user_id: int) -> dict:
    rows = db.query(Follow).filter(
        Follow.followed_id == user_id
    ).all()

    ids = [row.follower_id for row in rows]
    return {"user_id": user_id, "follower_ids": ids, "total": len(ids)}


def get_following(db: Session, user_id: int) -> dict:
    rows = db.query(Follow).filter(
        Follow.follower_id == user_id
    ).all()

    ids = [row.followed_id for row in rows]
    return {"user_id": user_id, "following_ids": ids, "total": len(ids)}