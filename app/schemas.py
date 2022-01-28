from datetime import datetime
from pydantic import BaseModel


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