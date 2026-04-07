from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv
from urllib.parse import quote


load_dotenv()
POSTGRES_PASSWORD=os.getenv("POSTGRES_PASSWORD")
POSTGRES_PASSWORD=quote(POSTGRES_PASSWORD) #to handle special characters in password
POSTGRES_HOST=os.getenv("POSTGRES_HOST")
POSTGRES_DATABASE=os.getenv("POSTGRES_DATABASE")
POSTGRES_USER=os.getenv("POSTGRES_USER")


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
