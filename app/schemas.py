from datetime import datetime
from pydantic import BaseModel, EmailStr


class Post(BaseModel):
    title: str
    content: str
    published: bool = True


class PostResponse(BaseModel):
    title: str
    content: str
    published: bool
    created_at: datetime

    class Config:
        orm_mode=True


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
