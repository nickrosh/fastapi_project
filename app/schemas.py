from datetime import datetime
from pydantic import BaseModel, EmailStr
from pydantic.types import conint


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    email: EmailStr
    id: int
    created_at: datetime

    class Config:
        orm_mode=True


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Post(BaseModel):
    title: str
    content: str
    published: bool = True


class PostResponse(BaseModel):
    title: str
    content: str
    published: bool
    id: int
    created_at: datetime
    user_id: int
    owner: UserResponse

    class Config:
        orm_mode=True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: str | None


class Vote(BaseModel):
    post_id: int
    direction: conint(le=1)
    