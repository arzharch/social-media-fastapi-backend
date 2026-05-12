from fastapi import FastAPI,Depends
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from . import models
from .database import engine
from .routers import post, user, auth, vote

load_dotenv()

# models.Base.metadata.create_all(bind=engine)

app=FastAPI()


@app.get("/")
async def root():
    return "Hello, World!"

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True
)

app.include_router(router=post.router)
app.include_router(router=user.router)
app.include_router(router=auth.router)
app.include_router(router=vote.router)



