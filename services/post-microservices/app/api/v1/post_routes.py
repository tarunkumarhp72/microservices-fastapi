from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.post_schemas import PostCreate, PostResponse
from app.services.post_services import (
    create_post,
    delete_post,
    get_post,
    get_user_posts,
    get_posts_by_user_ids
)
from app.core.auth import get_current_user

router = APIRouter(prefix="/posts", tags=["Posts"])


@router.post("", response_model=PostResponse)
def create_new_post(
    post: PostCreate,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return create_post(post, int(current_user["sub"]), db)


@router.get("/bulk", response_model=list[PostResponse])
def get_bulk_posts(
    user_ids: str = Query(..., description="Comma separated user IDs"),
    limit: int = Query(20, le=100),
    # current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Bulk endpoint for feed-service.
    Called with ?user_ids=1,2,3,4&limit=20
    Returns posts from all users in ONE DB query.
    """
    ids = [int(i) for i in user_ids.split(",") if i.strip().isdigit()]
    if not ids:
        return []
    return get_posts_by_user_ids(ids, limit, db)


@router.get("/user/{user_id}", response_model=list[PostResponse])
def user_posts(
    user_id: int,
    limit: int = Query(20, le=100),
    offset: int = Query(0),
    # current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return get_user_posts(user_id, db)


@router.get("/{post_id}", response_model=PostResponse)
def get_single_post(
    post_id: int,
    # current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    post = get_post(post_id, db)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post


@router.delete("/{post_id}")
def remove_post(
    post_id: int,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    result = delete_post(post_id, int(current_user["sub"]), db)

    if result is None:
        raise HTTPException(status_code=404, detail="Post not found")

    if result is False:
        raise HTTPException(status_code=403, detail="Not allowed")

    return {"message": "Post deleted"}