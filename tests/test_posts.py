


def test_get_all_posts(authorized_client):
    response = authorized_client.get('/posts/')
    print(response.json())
    assert response.status_code == 200