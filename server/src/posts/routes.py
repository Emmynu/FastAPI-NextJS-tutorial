from fastapi import APIRouter,status, HTTPException,Header, Depends
# from src.posts.db import posts 
from src.posts.schema import PostModel, PostUpdateModel, PostCreateModel
from src.db.main import session
from sqlmodel.ext.asyncio.session import AsyncSession
from src.posts.services import PostService
from src.db.models import Post
from sqlmodel import select, and_
from sqlalchemy.exc import SQLAlchemyError
from typing import List
from src.auth.dependencies import TokenBearer

router = APIRouter()
posts = PostService()
tokenBearer =  TokenBearer()

@router.post("/", status_code=status.HTTP_201_CREATED)
async def createPost(postData:PostCreateModel, session:AsyncSession = Depends(session), userDetails=Depends(tokenBearer)):
    # return userDetails
       try:
              userId = userDetails["user"]["id"]
              newPost = await posts.createPost(userId, postData, session)
              return newPost
       except SQLAlchemyError:
           raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="An occured! Please try again")
   

@router.get("/", status_code=status.HTTP_200_OK)
async def getAllPosts(session:AsyncSession = Depends(session), userDetails=Depends(tokenBearer)) :

    allPosts = await posts.getAllPost(session)

    if (allPosts != []):
        return allPosts
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not Found!")
       

@router.get("/{userId}", status_code=status.HTTP_200_OK, response_model=List[PostModel])
async def getUsersPost(userId:str, session:AsyncSession = Depends(session), userDetails=Depends(tokenBearer)):

    allPosts = await posts.getCurrentUserPost(userId, session)
    
    if (allPosts != []):
        return allPosts
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not Found!")
     

@router.get("/{userId}/{id}", status_code=status.HTTP_200_OK,  response_model=PostModel)
async def getPost(id:str, userId:str, session: AsyncSession = Depends(session), userDetails=Depends(tokenBearer)) -> dict :

    try:
        result = await session.exec(select(Post).where(and_(Post.userId == userId, Post.uid == id)))

        post = result.first()

        if not post:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Book with ID:{id} not Found!")
            
        return post
        
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Book with ID:{id} not Found!")
         
    

@router.delete("/{userId}/{id}", status_code=status.HTTP_200_OK)
async def deletePost(id:str, userId:str, session:AsyncSession = Depends(session), userDetails=Depends(tokenBearer)) -> dict:
   try:
       await posts.deletePost(postUid=id, userId=userId, session=session)
       return {"msg": "Post deleted successfully"}
   except:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error occured! Please try again")
       
           


@router.patch("/{id}", response_model=PostModel)
async def updatePost(id:str, postData:PostUpdateModel, session:AsyncSession = Depends(session), userDetails=Depends(tokenBearer)):
        await posts.updatePost(id, postData, session)

   
    


@router.get("/headers")
async def getHeaders(
    accept:str = Header(None),
    contentType:str = Header(None)
):
    req = {}
    req["Accept"] = accept
    req["Content-Type"] = contentType

    return req