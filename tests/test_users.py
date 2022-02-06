from jose import jwt
from app import schemas
from app.config import settings


def test_create_user(client, test_user):
    response = client.post("/users/", json={"email": "hello123@hotmale.com",
                                            "password": "password123"})

    new_user = schemas.UserResponse(**response.json())
    assert new_user.email == "hello123@hotmale.com"
    assert response.status_code == 201


def test_login_user(client, test_user):
    response = client.post("/login", data={"username": test_user['email'],
                                            "password": test_user['password']})
    login_response = schemas.Token(**response.json())
    payload = jwt.decode(login_response.access_token, settings.SECRET_KEY,
                         algorithms=[settings.ALGORITHM])
    id: str = payload.get('user_id')
    assert id == test_user['id']
    assert login_response.token_type == 'bearer'
    assert response.status_code == 200


def test_incorrect_login(client, test_user):
    response = client.post('/login', data={'username': test_user['email'], 
                                           'password': 'wrongpassword'})

    assert response.status_code == 403
    assert response.json().get('detail') == 'Invalid Credentials'