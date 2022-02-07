from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from fastapi.testclient import TestClient
import pytest
from app.main import app
from app.config import settings
from app.database import get_db
from app import models, oauth2


SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.DATABASE_USER}:{settings.DATABASE_PASSWORD}@{settings.DATABASE_HOSTNAME}:{settings.DATABASE_PORT}/{settings.DATABASE_NAME}_test'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


@pytest.fixture
def session():
    # before our tests drop all tables so we have a clean slate, then create
    # all tables. This way we can also see the tables after the tests are done.
    models.Base.metadata.drop_all(bind=engine)
    models.Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)


@pytest.fixture
def test_user(client):
    user_data = {"email": "test@test.com",
                 "password": "password"}
    response = client.post('/users/', json=user_data)
    assert response.status_code == 201
    new_user = response.json()
    new_user['password'] = user_data['password']
    return new_user


@pytest.fixture
def second_test_user(client):
    user_data = {"email": "test123@test.com",
                 "password": "password"}
    response = client.post('/users/', json=user_data)
    assert response.status_code == 201
    new_user = response.json()
    new_user['password'] = user_data['password']
    return new_user


@pytest.fixture
def token(test_user):
    return oauth2.create_access_token({"user_id": test_user['id']})


@pytest.fixture
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }
    return client
    

@pytest.fixture
def test_posts(test_user, second_test_user, session):
    posts_data = [{
        "title": "first title",
        "content": "first content",
        "user_id": test_user['id']
    },
    {
        "title": "second title",
        "content": "second content",
        "user_id": test_user['id']
    },
    {
        "title": "third title",
        "content": "third content",
        "user_id": test_user['id']
    },
    {
        "title": "fourth title",
        "content": "fourth content",
        "user_id": second_test_user['id']
    }]

    def create_post_model(posts) -> models.Post:
        return models.Post(**posts)

    post_map_list = list(map(create_post_model, posts_data))
    session.add_all(post_map_list)
    session.commit()
    
    posts = session.query(models.Post).all()
    return posts
    