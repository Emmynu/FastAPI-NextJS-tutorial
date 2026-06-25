from sqlalchemy.ext.asyncio.session import AsyncSession
from .schema import ReviewsCreateModel
from src.db.models import Reviews, Post
from sqlmodel import select


class ReviewService():
    async def createReview(self, userId:str, postId:str, session:AsyncSession, reviewModel:ReviewsCreateModel ):
        posts = await session.exec(select(Post).where(Post.uid == postId))
        postId = posts.first().uid
        
        newReview = Reviews(
            title=reviewModel.title,
            rating = reviewModel.rating,
            userId=userId,
            postId=postId
        )

        session.add(newReview)
        await session.commit()
        await session.refresh(newReview)

        return newReview