from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class PostBase(BaseModel):
    title:str
    content:str
    published: bool = True


class PostCreate(PostBase):
    pass # inherits all from Postbase


class Post(PostBase):
    id:int
    created_at: datetime

    class Config:
        orm_mode=True  #ensures that pydantic model reads data even if it not dict.

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class User(BaseModel):
    email: EmailStr
    id: int
    created_at : datetime


class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None
