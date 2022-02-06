from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from fastapi.testclient import TestClient
import pytest
from app.main import app
from app import schemas, models
from app.config import settings
from app.database import get_db


SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.DATABASE_USER}:{settings.DATABASE_PASSWORD}@{settings.DATABASE_HOSTNAME}:{settings.DATABASE_PORT}/{settings.DATABASE_NAME}_test'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


models.Base.metadata.create_all(bind=engine)


client = TestClient(app)


def test_root():
    res = client.get('/')
    assert res.json().get('message') == 'Welcome to the API!!'
    assert res.status_code == 200


def test_create_user():
    response = client.post("/users/", json={"email": "hello123456@hotmale.com",
                                            "password": "password123"})

    new_user = schemas.UserResponse(**response.json())
    assert new_user.email == "hello123456@hotmale.com"
    assert response.status_code == 201
