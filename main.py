from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional


app=FastAPI()

class Post(BaseModel):
    title :str
    content : str
    pulbished : bool = False
    rating: Optional[int] = None



@app.get("/")
async def root():
    return "Hello, World!"


@app.post("/create_posts")
async def create_posts(new_post : Post):
    print(new_post) 
    return {"data" : new_post}