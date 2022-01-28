from random import randrange
import os
import time

from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv
from app import models
from app.database import engine, get_db
from sqlalchemy.orm import Session

load_dotenv()

app = FastAPI()

models.Base.metadata.create_all(bind=engine)


retries = 5
while retries > 0:
    try:
        connection = psycopg2.connect(
            host="host.docker.internal",
            database="fastapi",
            user=os.getenv("POSTGRES_USER"),
            password=os.getenv("POSTGRES_PASSWORD"),
            cursor_factory=RealDictCursor
        )
        cursor = connection.cursor()
        print("database connection established")
        # cursor.close()
        # connection.close()
        break

    except ConnectionError as error:
        print("database connection failed")
        print(f"Error: {error}")
        retries -= 1
        time.sleep(2)


class Post(BaseModel):
    title: str
    content: str
    published: bool = True


my_posts = [
    {"title": "title of post 1", "content": "content of post 1", "id": 1},
    {"title": "title of post 2", "content": "content of post 2", "id": 2}
    ]


def find_post(id):
    for p in my_posts:
        if p['id'] == id:
            return p


def find_post_index(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i


@app.get("/")
def root():
    return {"message": "SANDOSIUS"}


@app.get("/sqlalchemy")
def test_posts(db: Session = Depends(get_db)):
    db.query(Post)
    return {"message": "it worked"}


@app.get("/posts")
def get_posts():
    cursor.execute("""SELECT * FROM POSTS""")
    posts = cursor.fetchall()
    return {"data": posts}


@app.get("/posts/{id}")
def get_post(id: int):
    cursor.execute("""SELECT * FROM POSTS WHERE id = %s""", (str(id),))
    post_detail = cursor.fetchone()
    if not post_detail:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")

    return {"post_detail": post_detail}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    cursor.execute(
    """INSERT INTO POSTS (title, content, published) VALUES (%s, %s, %s)
    RETURNING *""",
    (post.title, post.content, post.published))
    new_post = cursor.fetchone()
    connection.commit()
    return {"new_post": new_post}


@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s
                      WHERE id = %s RETURNING *""",
                      (post.title, post.content, post.published, str(id)))

    updated_post = cursor.fetchone()
    connection.commit()

    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id {id} does not exist")

    return {"data": updated_post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute("""DELETE FROM POSTS WHERE id = %s RETURNING *""",
                  (str(id)))
    deleted_post = cursor.fetchone()
    connection.commit()
    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id {id} does not exist")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
