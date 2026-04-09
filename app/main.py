from fastapi import FastAPI, Response, status, HTTPException,Depends
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
import psycopg2
import os
from psycopg2.extras import RealDictCursor
import time
from dotenv import load_dotenv
from . import models
from .database import engine, get_db
from sqlalchemy.orm import Session


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



class Post(BaseModel):
    title :str
    content : str
    published : bool = False

my_posts=[{"title":"title of post 1", "content":"content of post 1", "id":1},
          {"title":"title of post 2", "content":"content of post 2", "id":2} ]

def find_post(id):
    for p in my_posts:
        if p['id'] == id:
            return p
        
def find_index_post(id):
    for i, p  in enumerate(my_posts):
        if p["id"]==id:
            return i
        




@app.get("/")
async def root():
    return "Hello, World!"

@app.get("/posts")
async def get_posts(db: Session = Depends(get_db)):
    
    posts=db.query(models.Post).all() #gets all the rows

    return {"data": posts}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
async def create_posts(post : Post, db: Session  =Depends(get_db)): 

    new_post=models.Post(**post.dict())
    db.add(new_post)
    db.commit() 
    db.refresh(new_post) 

    
    return {"data" : new_post}

@app.get("/posts/latest")
async def get_latest_post():
    return my_posts[-1]

@app.get("/posts/{id}",status_code=status.HTTP_200_OK)
async def get_post(id: int, db: Session = Depends(get_db)):

    post = db.query(models.Post).filter(models.Post.id == id).first()
    print(post)

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id = {id} was not found")
    
    return {"data":post}


@app.put("/posts/{id}",status_code=status.HTTP_200_OK)
async def update_post(id: int, post: Post, db : Session = Depends(get_db)): #Post is used here so that it sticks to the schema defined in Post class
    
    post_query= db.query(models.Post).filter(models.Post.id == id)

    if not post_query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The post with the id = {id} was not found")
    post_dict=post.dict()
    post_query.update(post_dict)
    db.commit()


    return {"data":post_query.first()}


@app.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int, db : Session = Depends(get_db)):
    
    post_query = db.query(models.Post).filter(models.Post.id == id)
    if not post_query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id = {id} was not found")
    
    post_query.delete()
    db.commit()


    return Response(status_code=status.HTTP_204_NO_CONTENT)