from pydantic import BaseModel
from pydantic import EmailStr


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr

    class Config:
        from_attributes = True



class LoginRequest(BaseModel):
    email: str
    password: str



class FollowResponse(BaseModel):
    message: str


class FollowerUser(BaseModel):
    """Compact user info returned in follower/following lists."""
    id: int
    username: str
    email: str

    class Config:
        from_attributes = True


class FollowersListResponse(BaseModel):
    total: int
    users: list[FollowerUser]


class FollowingListResponse(BaseModel):
    total: int
    users: list[FollowerUser]