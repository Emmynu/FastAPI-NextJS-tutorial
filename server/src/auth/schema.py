from pydantic import BaseModel, Field
from datetime import datetime
import uuid
from typing import List
from src.posts.schema import PostModel
from src.reviews.schema import  ReviewsModel


class UserCreateModel(BaseModel):
    username:str = Field(min_length=3)
    email:str 
    password:str = Field(max_length=12)
    firstName:str
    lastName:str


class UserLoginModel(BaseModel):
    email:str 
    password:str 


class UserModel(BaseModel):
    uid:uuid.UUID 
    username:str
    email:str
    firstName:str
    lastName:str
    firstName:str = Field(default=False)
    password:str = Field(exclude=True)
    createdAt: datetime 
    updtedAt: datetime 
    post: List[PostModel]
    reviews: List[ReviewsModel]

class EmailsModel(BaseModel):
    address: List[str]