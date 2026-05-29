
from urllib.parse import quote
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.config import settings
from app import models, oauth2
from app.database import get_db
import pytest
from app.main import app
from fastapi.testclient import TestClient


POSTGRES_USER = settings.POSTGRES_USER
POSTGRES_PASSWORD = quote(settings.POSTGRES_PASSWORD) #quote is used to encode special characters    
POSTGRES_HOST = settings.POSTGRES_HOST
POSTGRES_DATABASE = settings.POSTGRES_DATABASE

SQLALCHEMY_DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}/fastapi_test"

engine= create_engine(SQLALCHEMY_DATABASE_URL) 

TestSessionLocal= sessionmaker(autocommit=False,autoflush=False, bind=engine) #default setup values

Base= declarative_base() 



@pytest.fixture()
def session():
    models.Base.metadata.drop_all(bind=engine)
    models.Base.metadata.create_all(bind=engine)
    #command.downgrade("base") with alembic
    #command.upgrade("head")
    
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture()
def client(session):
    #dependency to get DB session
    def override_get_db():
        db=TestSessionLocal()
        try:
            yield session
        finally:
            session.close()
    
    app.dependency_overrides[get_db] = override_get_db
    
    yield TestClient(app)
    

@pytest.fixture(scope="function")
def test_user(client):
    user_data = {"email" : "test@example.com", "password": "password@123"}
    res = client.post("/users", json = user_data)
    assert res.status_code == 201

    new_user = res.json()
    new_user['password'] = user_data['password']

    return new_user

@pytest.fixture(scope="function")
def test_user2(client):
    user_data = {"email" : "test1@example.com", "password": "password@123"}
    res = client.post("/users", json = user_data)
    assert res.status_code == 201

    new_user = res.json()
    new_user['password'] = user_data['password']

    return new_user

@pytest.fixture
def token(test_user):
    return oauth2.create_access_token(data={"user_id": test_user['id']})


@pytest.fixture
def authorized_client(session, token):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db
    test_client = TestClient(app)
    test_client.headers = {
        **test_client.headers,
        "Authorization": f"Bearer {token}"
    }

    return test_client


@pytest.fixture
def test_posts(test_user, authorized_client, test_user2):
    post_data = [
        {"title": "First Post", "content": "Content of the first post", "user_id": test_user['id']},
        {"title": "Second Post", "content": "Content of the second post", "user_id": test_user['id']},
        {"title": "Third Post", "content": "Content of the third post", "user_id": test_user['id']},
        {"title": "Fourth Post", "content": "Content of the fourth post", "user_id": test_user2['id']},
        {"title": "Fifth Post", "content": "Content of the fifth post", "user_id": test_user2['id']}
    ]
    posts = []
    for data in post_data:
        res = authorized_client.post("/posts", json=data)
        posts.append(res.json())

    return posts
