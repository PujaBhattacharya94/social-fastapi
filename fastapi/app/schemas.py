from typing import Annotated, Optional
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from pydantic.types import conint

class Post_Base(BaseModel):
    title: str
    content: str
    published: bool = True
    #rating: Optional[int] = None

class PostCreate(Post_Base):
    pass


class UserCreateResponse(BaseModel):
    id: int
    email:EmailStr
    created_at : datetime
    class Config:
        orm_mode = True



class PostResponse(Post_Base):
    id: int
    created_at : datetime
    owner_id : int
    #return the user detail based on owner_id
    owner: UserCreateResponse
    #convert the schema into a dict because pydentic only reads a dictationary
    class Config:
        orm_mode = True

class PostResponseVote(BaseModel):
    Post: PostResponse
    votes: int


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token : str
    token_type : str

class TokenData(BaseModel):
    id : Optional[int] = None


class Vote(BaseModel):
    post_id : int
    dir: Annotated[int, Field(ge=0, le=1)]

