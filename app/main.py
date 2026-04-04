from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
import psycopg2
import os
from psycopg2.extras import RealDictCursor
import time
from dotenv import load_dotenv

load_dotenv()


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
    rating: Optional[int] = None

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
async def get_posts():
    return my_posts

@app.post("/posts", status_code=status.HTTP_201_CREATED)
async def create_posts(post : Post): 
    post_dict=post.dict() 
    post_dict['id']=randrange(0,1000000)
    my_posts.append(post_dict)
    return {"data" : post_dict}

@app.get("/posts/latest")
async def get_latest_post():
    return my_posts[-1]

@app.get("/posts/{id}",status_code=status.HTTP_200_OK)
async def get_post(id: int, response: Response):
    
    
    if not find_post(id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")

    return {"data":find_post(id)}


@app.put("/posts/{id}",status_code=status.HTTP_200_OK)
async def update_post(id: int, post: Post): #post is used here so that it sticks to the schema defined in Post class
    index=find_index_post(id)
    if index is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist") 
    
    post_dict=post.dict()
    post_dict['id']=id
    my_posts[index]=post_dict
    return {"data":post_dict}


@app.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int):
    index=find_index_post(id)
    if index is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist") 
    my_posts.pop(index)

    return Response(status_code=status.HTTP_204_NO_CONTENT)