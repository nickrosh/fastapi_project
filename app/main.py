from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app import models
from app.database import engine
from .routers import post, user, auth, vote


# initialization settings
app = FastAPI()


origins = [
    "http://localhost:8000",
    "https://www.google.com"
]

# CORS settings and what to allow
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=['*'],
#     allow_headers=['*']
# )


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)


# auto generates tables, not needed when using Alembic
# models.Base.metadata.create_all(bind=engine)


@app.get("/")
def root():
    return {"message": "Welcome to the API"}
