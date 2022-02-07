import imp
from typing import List
from app import schemas

def test_get_all_posts(authorized_client, test_posts):
    response = authorized_client.get('/posts/')

    def validate(post: dict) -> schemas.PostOut:
        return schemas.PostOut(**post)
    posts_map = map(validate, response.json())
    posts_list = list(posts_map)
    assert len(response.json()) == len(test_posts)
    assert response.status_code == 200
    # assert posts_list[0].Post.id == test_posts[0].id


def test_get_one_post(authorized_client, test_posts):
    response = authorized_client.get(f'/posts/{test_posts[0].id}')
    post = schemas.PostOut(**response.json())
    assert post.Post.id == test_posts[0].id
    assert post.Post.content == test_posts[0].content
    assert post.Post.title == test_posts[0].title
    assert response.status_code == 200


def test_unauthorized_user_get_all_posts(client, test_posts):
    response = client.get('/posts/')
    assert response.status_code == 401


def test_unauthorized_user_get_one_post(client, test_posts):
    response = client.get(f'/posts/{test_posts[0].id}')
    assert response.status_code == 401


def test_get_one_post_not_exist(authorized_client, test_posts):
    response = authorized_client.get(f'/posts/1234567')
    assert response.status_code == 404


