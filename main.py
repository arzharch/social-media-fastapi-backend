from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange

app=FastAPI()

class Post(BaseModel):
    title :str
    content : str
    pulbished : bool = False
    rating: Optional[int] = None

my_posts=[{"title":"title of post 1", "content":"content of post 1", "id":1},
          {"title":"title of post 2", "content":"content of post 2", "id":2} ]


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

@app.get("/posts/{id}")
async def get_post(id: int, response: Response):
    for post in my_posts:
        if post['id'] == id:
            return {"post_detail": post}
    #response.status_code = status.HTTP_404_NOT_FOUND

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")

    return
