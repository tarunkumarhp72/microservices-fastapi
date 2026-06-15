from datetime import datetime
from pydantic import BaseModel


class FollowResponse(BaseModel):
    message: str


class FollowRecord(BaseModel):
    follower_id: int
    followed_id: int
    created_at: datetime

    class Config:
        from_attributes = True


class FollowingIdsResponse(BaseModel):
    user_id: int
    following_ids: list[int]
    total: int


class FollowersIdsResponse(BaseModel):
    user_id: int
    follower_ids: list[int]
    total: int