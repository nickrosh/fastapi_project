from app import schemas
from tests.database import client, session


def test_root(client):
    res = client.get('/')
    assert res.json().get('message') == 'Welcome to the API!!'
    assert res.status_code == 200


def test_create_user(client):
    response = client.post("/users/", json={"email": "hello123@hotmale.com",
                                            "password": "password123"})

    new_user = schemas.UserResponse(**response.json())
    assert new_user.email == "hello123@hotmale.com"
    assert response.status_code == 201
