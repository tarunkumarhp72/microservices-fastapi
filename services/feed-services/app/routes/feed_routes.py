from fastapi import APIRouter

from app.services.feed_services import generate_feed


router = APIRouter(
    prefix="/feed",
    tags=["Feed"]
)


@router.get("/{user_id}")
def get_feed(user_id: int):

    return generate_feed(user_id)