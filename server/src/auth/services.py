from src.db.models import Users
from .schema import UserCreateModel, ResetPasswordModel
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlmodel import select, update
# from sqlalchemy.orm import selectinload
from .utilis import generatePasswordHash

class UserService:
    async def getUser(self,email:str, session:AsyncSession):
        result = await session.exec(select(Users).where(Users.email == email))

        user = result.first()

        return user if user is not None else None
    
    async def userExists(self, email:str, session:AsyncSession):
        user = await self.getUser(email, session)

        return True if user is not None else False 


    async def creatUser(self, userData:UserCreateModel, session:AsyncSession):
        newUser = Users(
            email=userData.email,
            username=userData.username,
            password= generatePasswordHash(userData.password),
            firstName=userData.firstName,
            lastName=userData.lastName
            )
        
        session.add(newUser)
        await session.commit()
        await session.refresh(newUser)
        
        return newUser
    
    async def updateUserPassword(self,session: AsyncSession, email:str, passwordData:ResetPasswordModel):
        newPassword = generatePasswordHash(passwordData.newPassword)
        
        statement = await session.exec(update(Users).where(Users.email == email).values(password = newPassword))

        await session.commit()

        return True if statement is not None else False