from multiprocessing import synchronize
from random import randrange
import os
import time

from typing import Optional, List
from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv
from sqlalchemy.orm import Session

from app import models, schemas, utils
from app.database import engine, get_db

# load_dotenv()

# initialization settings
app = FastAPI()
models.Base.metadata.create_all(bind=engine)



# retries = 5
# while retries > 0:
#     try:
#         connection = psycopg2.connect(
#             host="host.docker.internal",
#             database="fastapi",
#             user=os.getenv("POSTGRES_USER"),
#             password=os.getenv("POSTGRES_PASSWORD"),
#             cursor_factory=RealDictCursor
#         )
#         cursor = connection.cursor()
#         print("database connection established")
#         # cursor.close()
#         # connection.close()
#         break

#     except ConnectionError as error:
#         print("database connection failed")
#         print(f"Error: {error}")
#         retries -= 1
#         time.sleep(2)





# my_posts = [
#     {"title": "title of post 1", "content": "content of post 1", "id": 1},
#     {"title": "title of post 2", "content": "content of post 2", "id": 2}
#     ]


# def find_post(id):
#     for p in my_posts:
#         if p['id'] == id:
#             return p


# def find_post_index(id):
#     for i, p in enumerate(my_posts):
#         if p['id'] == id:
#             return i


@app.get("/")
def root():
    return {"message": "Welcome to the API"}


@app.get("/posts", response_model=List[schemas.PostResponse])
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts


@app.get("/posts/{id}", response_model=schemas.PostResponse)
def get_post(id: int, db: Session = Depends(get_db)):
    post_detail = db.query(models.Post).filter(models.Post.id == id).first()

    if not post_detail:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")

    return post_detail


@app.post("/posts", status_code=status.HTTP_201_CREATED, 
          response_model=schemas.PostResponse)
def create_post(post: schemas.Post, db: Session = Depends(get_db)):
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


@app.put("/posts/{id}", response_model=schemas.PostResponse)
def update_post(id: int, post: schemas.Post, db: Session = Depends(get_db)):
    updated_post = db.query(models.Post).filter(models.Post.id == id)

    if updated_post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id {id} does not exist")

    updated_post.update(post.dict(),
         synchronize_session=False)

    db.commit()

    return updated_post.first()


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    deleted_post = db.query(models.Post).filter(models.Post.id == id)

    if deleted_post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id {id} does not exist")

    deleted_post.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.get("/users/{id}", response_model=schemas.UserResponse)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"User with id: {id}")
    return user

@app.post("/users", status_code=status.HTTP_201_CREATED,
          response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user
