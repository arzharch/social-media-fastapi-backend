from pydantic import BaseModel
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