from fastapi import APIRouter, Query
from app.services.feed_services import generate_feed

router = APIRouter(prefix="/feed", tags=["Feed"])


@router.get("/{user_id}")
def get_feed(
    user_id: int,
    limit: int = Query(20, le=100),   
    offset: int = Query(0)             
):
    return generate_feed(user_id, limit=limit, offset=offset)