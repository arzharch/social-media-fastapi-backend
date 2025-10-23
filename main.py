from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel



app=FastAPI()

class Post(BaseModel):
    title :str
    content : str



@app.get("/")
async def root():
    return "Hello, World!"


@app.post("/create_posts")
async def create_posts(new_post : Post):
    print(new_post)
    return { "title":new_post.title, "content": new_post.content}