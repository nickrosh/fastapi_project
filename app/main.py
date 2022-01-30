from multiprocessing import synchronize
from random import randrange
import os
import time

from fastapi import FastAPI
from app import models
from app.database import engine
from .routers import post, user, auth

# initialization settings
app = FastAPI()
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)

models.Base.metadata.create_all(bind=engine)


@app.get("/")
def root():
    return {"message": "Welcome to the API"}
