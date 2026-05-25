from fastapi.testclient import TestClient
from app import schemas
from app.database import get_db
from app.main import app
from app import models
import pytest
from alembic import command
from app import schemas
from app import oauth2
import jwt
from app.config import settings




def test_root(client):

    response = client.get("/")
    assert response.status_code == 200

def test_create_user(client):

    res = client.post("/users", json = {"email": "test@example.com", "password": "password123"})
    new_user = schemas.User(**res.json())

    assert res.status_code == 201
    assert res.json().get("email") == "test@example.com"
    assert res.json().get("id") == new_user.id


def test_login(client, test_user):

    res = client.post("/login", data= {"username":test_user['email'], "password":test_user['password']})
    #user = schemas.UserLogin(**res.json())

    login_res = schemas.Token(**res.json())

    payload = jwt.decode(login_res.access_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])

    user_id = payload.get("user_id")
    assert login_res.token_type == "bearer"
    assert user_id == test_user['id']

    assert res.status_code == 200
                                      