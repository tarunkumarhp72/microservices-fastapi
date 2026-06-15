from datetime import datetime

from pydantic import BaseModel


class PostCreate(BaseModel):
    content: str


class PostResponse(BaseModel):
    id: int
    user_id: int
    content: str
    created_at: datetime 

    class Config:
        from_attributes = True