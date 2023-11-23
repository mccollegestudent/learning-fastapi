from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, List
#from datatime import datatime

from pydantic.types import conint

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True # default value

class PostCreate(PostBase): #inheritance 
    pass

class UserOut(BaseModel):
    id: int 
    email: EmailStr
    created_at: datetime

    class Config: #sql alchemy mode we get we need pydatic to convert it into a regular model
        orm_mode = True
        
class Post(PostBase):
    id:int
    created_at: datetime
    owner_id: int
    owner: UserOut

    class Config:
        orm_mode = True

class PostOut(BaseModel):
    Post: Post                              #capitalze this for some reason
    votes: int

    class Config:
        orm_mode = True

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel): #not working for some reason
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None

class Vote(BaseModel):
    post_id: int
    dir: conint(le=1, ge=0)

