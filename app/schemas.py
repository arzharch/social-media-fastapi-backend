from pydantic import BaseModel, EmailStr, conint
from typing import Optional
from datetime import datetime

class PostBase(BaseModel):
    title:str
    content:str
    published: bool = True


class PostCreate(PostBase):
    pass # inherits all from Postbase

class User(BaseModel):
    email: EmailStr
    id: int
    created_at : datetime



class Post(PostBase):
    id:int
    user_id: int
    created_at: datetime
    owner: User

    class Config:
        orm_mode=True  #ensures that pydantic model reads data even if it not dict.

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str



class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[int] = None


class Vote(BaseModel):
    post_id: int
    dir: int