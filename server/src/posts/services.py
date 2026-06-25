from sqlmodel.ext.asyncio.session import AsyncSession
from .schema import PostCreateModel
from sqlmodel import select, desc, delete, update, and_
from src.db.models import Post
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException, status

class PostService():

    async def createPost(self, userId:str, postData:PostCreateModel, session:AsyncSession):
       
        newPost = Post(
                userId=userId,
                title= postData.title,
                body= postData.body
            )

        session.add(newPost)
        await session.commit()
        await session.refresh(newPost)

        return newPost

    async def getAllPost(self, session:AsyncSession):
        try:
            result = await session.exec(select(Post).order_by(desc(Post.createdAt)))

            posts =  result.all()
            
            return posts if posts is not None else None
        
        except SQLAlchemyError:
            await session.rollback()
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Book not Found!")
        
        except Exception :
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="An error occured")
        
    async def getCurrentUserPost(self, userId:str, session:AsyncSession):
        try:
            result = await session.exec(select(Post).where(Post.userId == userId).order_by(desc(Post.createdAt)))

            posts =  result.all()
            
            return posts if posts is not None else None
        
        except SQLAlchemyError:
            await session.rollback()
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Book not Found!")
        
        except Exception :
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="An error occured")


    async def updatePost(self, postUid:str, postUpdateData:PostCreateModel, session:AsyncSession):
         try:
                result = await session.exec(update(Post).where(Post.uid == postUid).values(title = postUpdateData.title, body = postUpdateData.body))

                await session.commit()
                await session.refresh(result.first())

                return result.first()
         except SQLAlchemyError:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Error occured while updating book!")
        
    

    async def deletePost(self,userId:str, postUid:str, session:AsyncSession):
        await session.exec(delete(Post).where(and_(Post.uid == postUid, Post.userId == userId)))
        await session.commit()
