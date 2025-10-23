from fastapi import FastAPI
from fastapi.params import Body



app=FastAPI()

@app.get("/")
async def root():
    return "Hello, World!"


@app.post("/create_posts")
async def create_posts(payLoad: dict = Body(...)):
    print(payLoad)
    return { "new_post":f"title {payLoad['title']} and the content is {payLoad['content']}"}