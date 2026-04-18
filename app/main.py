from fastapi import FastAPI, Response, status, HTTPException,Depends
import psycopg2
import os
from psycopg2.extras import RealDictCursor
import time
from dotenv import load_dotenv
from . import models
from .database import engine
from .routers import post, user, auth

load_dotenv()

models.Base.metadata.create_all(bind=engine)

app=FastAPI()


while True:
    try:
        conn=psycopg2.connect(host=os.getenv("POSTGRES_HOST"), database=os.getenv("POSTGRES_DATABASE"),user=os.getenv("POSTGRES_USER"), password=os.getenv("POSTGRES_PASSWORD"), cursor_factory=RealDictCursor)

        cursor=conn.cursor()

        print("Database connection was successful")
        break

    except Exception as error:
        print(f"Database connection failued due to {error}")
        time.sleep(2)


@app.get("/")
async def root():
    return "Hello, World!"


app.include_router(router=post.router)
app.include_router(router=user.router)
app.include_router(router=auth.router)



