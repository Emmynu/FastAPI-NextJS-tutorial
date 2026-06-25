from sqlmodel import SQLModel, Field, Column, Relationship
import sqlalchemy.dialects.postgresql as pg
from datetime import datetime
import uuid
from typing import Optional,List


class Users(SQLModel, table=True):
    __tablename__ = "Users"

    uid:uuid.UUID = Field(
        sa_column=Column(
            pg.UUID,
            nullable=False,
            primary_key=True,
            default=uuid.uuid4
        )
    )
    username:str
    email:str
    firstName:str
    lastName:str
    password:str = Field(exclude=True)

    post: List["Post"] = Relationship(back_populates="user", sa_relationship_kwargs={"lazy": "selectin"})
    reviews: List["Reviews"] = Relationship(back_populates="user", sa_relationship_kwargs={"lazy": "selectin"})
    createdAt: datetime = Field(
        sa_column=Column(
            pg.TIMESTAMP,
            default=datetime.now()
        )
    )
    updtedAt: datetime = Field(
    sa_column=Column(
        pg.TIMESTAMP,
        default=datetime.now()
    )
)
    
def __repr__(self):
    return f"<User {self.username}>"




class Post(SQLModel, table=True):
    __tablename__ = "Posts"

    uid:uuid.UUID = Field(
        sa_column=Column(
            pg.UUID, 
            nullable=False,
            primary_key=True,
            default=uuid.uuid4
        )
    )
    userId:uuid.UUID = Field(default=None, foreign_key="Users.uid")
    user: Optional["Users"] = Relationship(back_populates="post", sa_relationship_kwargs={"lazy": "selectin"})
    reviews: List["Reviews"] = Relationship(back_populates="post", sa_relationship_kwargs={"lazy": "selectin"})

    title:str
    body:str

    # test:str
    
    createdAt:datetime = Field(
        sa_column=Column(pg.TIMESTAMP, default=datetime.now())
    )
    updatedAt:datetime = Field(
        sa_column=Column(pg.TIMESTAMP, default=datetime.now())
    )


def __repr__(self):
    return f"<Post {self.title}>"



class Reviews(SQLModel, table= True):
    __tablename__ = "Reviews"

    uid:uuid.UUID = Field(
        sa_column=Column(
            pg.UUID,
            default=uuid.uuid4,
            nullable=False,
            primary_key=True
        )
    )
    userId: uuid.UUID = Field(default=None, foreign_key="Users.uid") 
    postId: uuid.UUID = Field(default=None, foreign_key="Posts.uid")
    title: str = Field(default="Review title")
    rating: int = Field(lt=5)

    user: Optional["Users"] =  Relationship(back_populates="reviews", sa_relationship_kwargs={"lazy": "selectin"})
    post: Optional["Post"] =  Relationship(back_populates="reviews", sa_relationship_kwargs={"lazy": "selectin"})
    createdAt: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now()))
    updatedAt: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now()))

def __repr__(self):
    return f"<Reviews for {self.postId} by {self.userId}> "
