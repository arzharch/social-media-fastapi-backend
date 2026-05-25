
from urllib.parse import quote
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.config import settings
from app import models
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
    