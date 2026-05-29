


from typing import List
from app import models, schemas
import pytest

def test_get_all_posts(authorized_client, test_posts):

    res = authorized_client.get("/posts")
    def validate(post):
        return schemas.PostOut(**post)
    
    posts_map = map(validate, res.json())
    posts_lists= list(posts_map)


    assert res.status_code == 200

def test_unauthorized_user_get_all_posts(client, test_posts):

    res = client.get("/posts/")

    assert res.status_code == 401

def test_unauthorized_user_get_one_post(client, test_posts):

    res = client.get(f"/posts/1")
    print(res.json())

    assert res.status_code == 401

def test_get_one_post_not_exist(authorized_client, test_posts):

    res = authorized_client.get("/posts/9999")
    assert res.status_code == 404

def test_get_one_post(authorized_client, test_posts):

    res = authorized_client.get("/posts/1")
    assert res.status_code == 200



@pytest.mark.parametrize("title, content, published", [
    ("Test Post 1", "Content for test post 1", True),
    ("Test Post 2", "Content for test post 2", False),
    ("Test Post 3", "Content for test post 3", True)
])
def test_create_post(authorized_client, title, content, published):

    res = authorized_client.post("/posts", json={"title": title, "content": content, "published": published})

    created_Post = schemas.Post(**res.json())

    assert res.status_code == 201
    assert created_Post.title == title
    assert created_Post.content == content

def test_create_default_published_true(authorized_client, test_posts):

    res = authorized_client.post("/posts", json={"title": "Test Post 4", "content": "Content for test post 4"})
    created_Post = schemas.Post(**res.json())

    assert res.status_code == 201
    assert created_Post.title == "Test Post 4"
    assert created_Post.content == "Content for test post 4"
    assert created_Post.published == True

def test_unauthorized_user_create_post(client, test_posts):

    res = client.post("/posts", json={"title": "Unauthorized Post", "content": "This should not be created"})

    assert res.status_code == 401

def test_unauthorized_user_delete_post(client, test_posts):
    res = client.delete(f"/posts/{test_posts[0]['id']}")

    assert res.status_code == 401

def test_delete_post_success(authorized_client, test_posts):
    res = authorized_client.delete(f"/posts/{test_posts[0]['id']}")

    assert res.status_code == 204

def test_delete_post_not_exist(authorized_client, test_posts):
    res = authorized_client.delete("/posts/9999")

    assert res.status_code == 404


def test_delete_post_other_user_post(authorized_client, test_posts):
    res = authorized_client.delete(f"/posts/{test_posts[3]['id']}")

    assert res.status_code == 401

def test_update_post(authorized_client, test_posts):

    res = authorized_client.put(f"/posts/{test_posts[0]['id']}", json = {"title": "Updated Title", "content": "Updated Content", "published": False})
    updated_post = schemas.Post(**res.json())

    assert res.status_code == 200
    assert updated_post.title == "Updated Title"
    assert updated_post.content == "Updated Content"
    assert updated_post.published == False

def test_update_post_other_user_post(authorized_client, test_posts):

    res = authorized_client.put(f"/posts/{test_posts[3]['id']}", json = {"title": "Updated Title", "content": "Updated Content", "published": False})

    assert res.status_code == 401

def test_update_post_not_exist(authorized_client, test_posts):

    res = authorized_client.put("/posts/9999", json = {"title": "Updated Title", "content": "Updated Content", "published": False})

    assert res.status_code == 404

