from pydantic import BaseModel,EmailStr
from datetime import datetime

class Post(BaseModel):
    title: str
    content: str
    published: bool = True

class CreatePost(BaseModel):
    title: str
    content: str
    published: bool = True

class UpdatedPost(BaseModel):
    published: bool = True

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass

#Response
class Post(BaseModel):
    id: int
    
    created_at: datetime

#config file so pydantic model understands its sqlalchemy not a dict
#so we have to convert sqlalchemy model to pydantic model
    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    email: EmailStr
    password: str

#Respons
class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True






    
     