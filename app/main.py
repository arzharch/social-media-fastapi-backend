from fastapi import FastAPI,Depends
from dotenv import load_dotenv
from . import models
from .database import engine
from .routers import post, user, auth

load_dotenv()

models.Base.metadata.create_all(bind=engine)

app=FastAPI()


@app.get("/")
async def root():
    return "Hello, World!"


app.include_router(router=post.router)
app.include_router(router=user.router)
app.include_router(router=auth.router)



