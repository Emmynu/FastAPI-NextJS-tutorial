from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio.session import AsyncSession
from .service import ReviewService
from src.auth.dependencies import TokenBearer
from src.db.main import session
from .schema import ReviewsCreateModel

router = APIRouter()
reviews = ReviewService()
tokenBearer =  TokenBearer()

@router.post("/{postId}")
async def createReviews(postId, reviewsDataModel:ReviewsCreateModel, userDetails =  Depends(tokenBearer), session:AsyncSession=Depends(session)):
    userId =  userDetails["user"]["id"] # current user
    response = await reviews.createReview(userId, postId, reviewModel=reviewsDataModel, session=session)
    return response

@router.get("/{postId}")
async def getReviews():
    pass