import pytest
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


@pytest.mark.parametrize("title, content, published", [
    ("awesome new title", "new content", True),
    ("decent new title", "nu content", True),
    ("awesome old title", "old content", False)
    ])
def test_create_post(authorized_client, test_user, title, content, published):
    response = authorized_client.post('/posts/', 
        json={'title': title, 'content': content, 'published': published})

    created_post = schemas.PostResponse(**response.json())
    assert response.status_code == 201
    assert created_post.title == title
    assert created_post.content == content
    assert created_post.published == published
    assert created_post.user_id == test_user['id']


def test_create_post_default_published_true(authorized_client, test_user, test_posts):
    response = authorized_client.post('/posts/', 
        json={'title': "some title", 'content': "test content"})

    created_post = schemas.PostResponse(**response.json())
    assert response.status_code == 201
    assert created_post.title == "some title"
    assert created_post.content == "test content"
    assert created_post.published == True
    assert created_post.user_id == test_user['id']


def test_unauthorized_user_create_post(client, test_user, test_posts):
    response = client.post('/posts/', 
        json={'title': "some title", 'content': "test content"})
    assert response.status_code == 401


def test_delete_post_success(authorized_client, test_user, test_posts):
    response = authorized_client.delete(f'/posts/{test_posts[0].id}')
    assert response.status_code == 204


def test_unauthorized_delete_post(client, test_user, test_posts):
    response = client.delete(f'/posts/{test_posts[0].id}')
    assert response.status_code == 401


def test_delete_post_nonexistant(authorized_client, test_user, test_posts):
    response = authorized_client.delete('/posts/12345678')
    assert response.status_code == 404


def test_delete_post_other_user(authorized_client, test_user,
                                second_test_user, test_posts):
    response = authorized_client.delete(f'/posts/{test_posts[3].id}')
    assert response.status_code == 403