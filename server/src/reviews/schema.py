from pydantic import BaseModel
import uuid
from datetime import datetime

class ReviewsModel(BaseModel):
    
    uid:uuid.UUID
    userId: uuid.UUID 
    postId: uuid.UUID
    title: str
    rating: int 

    # user: Optional["Users"] =  Relationship(back_populates="reviews", sa_relationship_kwargs={"lazy": "selectin"})
    # posts: Optional["Post"] =  Relationship(back_populates="reviews", sa_relationship_kwargs={"lazy": "selectin"})
    createdAt: datetime
    updatedAt: datetime


class ReviewsCreateModel(BaseModel):
    title:str
    rating: int