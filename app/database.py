from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings
from dotenv import load_dotenv
from urllib.parse import quote


POSTGRES_USER = settings.POSTGRES_USER
POSTGRES_PASSWORD = quote(settings.POSTGRES_PASSWORD) #quote is used to encode special characters    
POSTGRES_HOST = settings.POSTGRES_HOST
POSTGRES_DATABASE = settings.POSTGRES_DATABASE

SQLALCHEMY_DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}/{POSTGRES_DATABASE}"

engine= create_engine(SQLALCHEMY_DATABASE_URL) 

SessionLocal= sessionmaker(autocommit=False,autoflush=False, bind=engine) #default setup values

Base= declarative_base() 


#dependency to get DB session
def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()
