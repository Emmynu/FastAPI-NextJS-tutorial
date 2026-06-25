from pydantic import BaseModel
import uuid
from datetime import datetime
from typing import List
from src.reviews.schema import ReviewsModel

class PostModel(BaseModel):
    uid:uuid.UUID
    userId:uuid.UUID
    title:str
    body:str
    reviews: List[ReviewsModel]
    createdAt:datetime 
    updatedAt:datetime 


class PostCreateModel(BaseModel):
    # userId:int
    title:str
    body:str

class PostUpdateModel(BaseModel):
    title:str
    body:str