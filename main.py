from typing import Optional
from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel


app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None


@app.get("/")
def root():
    return {"message": "SANDOSIUS"}


@app.get("/posts")
def get_posts():
    return {"post": "whatever"}


@app.post("/posts")
def create_posts(post: Post):
    print(post.rating)
    return {"new_post": post}
