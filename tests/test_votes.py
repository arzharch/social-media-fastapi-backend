

def test_vote_on_post(authorized_client, test_posts):

    res = authorized_client.post("/vote/", json={"post_id": 1, "dir": 1})

def test_vote_on_post_twice(authorized_client, test_posts):

    res = authorized_client.post("/vote/", json={"post_id": 1, "dir": 1})
    assert res.status_code == 201

    res = authorized_client.post("/vote/", json={"post_id": 1, "dir": 1})
    assert res.status_code == 409

def test_delete_vote_on_post(authorized_client, test_posts):

    res = authorized_client.post("/vote/", json={"post_id": 1, "dir": 1})
    assert res.status_code == 201

    res = authorized_client.post("/vote/", json={"post_id": 1, "dir": 0})
    assert res.status_code == 201

def test_delete_vote_on_post_not_exist(authorized_client):
    res = authorized_client.post("/vote/", json={"post_id": 9999, "dir": 0})
    assert res.status_code == 404

def test_vote_on_post_unauthorized(client, test_posts):

    res = client.post("/vote/", json={"post_id": 1, "dir": 1})
    assert res.status_code == 401

def test_delete_vote_on_post_unauthorized(client, test_posts):

    res = client.post("/vote/", json={"post_id": 1, "dir": 0})
    assert res.status_code == 401

def test_vote_delete_twice(authorized_client, test_posts):

    res = authorized_client.post("/vote/", json={"post_id": 1, "dir": 1})
    assert res.status_code == 201

    res = authorized_client.post("/vote/", json={"post_id": 1, "dir": 0})
    assert res.status_code == 201

    res = authorized_client.post("/vote/", json={"post_id": 1, "dir": 0})
    assert res.status_code == 404