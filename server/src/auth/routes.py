from fastapi import APIRouter, Depends, status, HTTPException, Response, Request
from .schema import UserCreateModel, UserLoginModel, UserModel,EmailsModel, ResetPasswordModel
from .services import UserService
from sqlalchemy.ext.asyncio.session  import AsyncSession
from src.db.main import session
from .utilis import createAccessToken, decodeToken, verifyHash, createIdnToken, decodeIdnToken
from datetime import timedelta
from src.auth.dependencies import TokenBearer
from src.mail import create_message, mail
import logging


router = APIRouter()
auth = UserService()
tokenBearer = TokenBearer() 


@router.post("/mail")
async def sendMailMessage(emails:EmailsModel):
    email_address = emails.address
    html = "<h1 style='color:blue'>Welcome to the app </h1>"

    message = create_message(
        recipients=email_address,
        subject="WELCOME",
        body=html
    )

    await mail.send_message(message)

    return { "msg": "Email sent successful" }




@router.post("/signup", status_code=status.HTTP_201_CREATED)
async def createUserAccount(userData:UserCreateModel, session: AsyncSession = Depends(session)):
    email = userData.email

    exists = await auth.userExists(email, session)

    if exists:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User already exists")
    else:
       try:
            newUser = await auth.creatUser(userData, session)

            return newUser
       except:
           raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="An error occured")



@router.post("/login")
async def login(loginData:UserLoginModel,  response:Response, session: AsyncSession =  Depends(session)):
    email =  loginData.email
    password =  loginData.password

    user = await auth.getUser(email, session)

    if user is not None:
        isValid =  verifyHash(password, user.password)

        if isValid:
            
            data = {
                "email": user.email,
                "id":  str(user.uid),
                "username": user.username
            }

            accessToken = createAccessToken(data, expiry=timedelta(days=0.5))
            refreshToken = createAccessToken(data, refresh=True, expiry=timedelta(days=7))

          
            response.set_cookie(
                key="accessToken",
                value=accessToken,
                httponly=True,
                samesite="none",
                path="/",
                secure=True,  #Todo: set True before deployment
                max_age=3600,
                # domain="http://localhost:3000/"
            )

            response.set_cookie(
                key="refreshToken",
                value=refreshToken,
                httponly=True,
                samesite="none",
                path="/",
                secure=True,  #Todo: set True before deployment
                max_age=3600,
                # domain="http://localhost:3000/"
            )

            
            return { "msg": "Login Successful", "user": user, "accessToken": accessToken}

        elif isValid is False:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Password")
  
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Email")
        

@router.post("/forgot-password")
async def forgotPassword(email:str, session: AsyncSession = Depends(session)):

    user = await auth.getUser(email, session)

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    try:
        token =  createIdnToken(email)

        Link = f"https://fast-api-next-js-tutorial.vercel.app/auth/reset-password?token={token}"

        html = f"""

        <h1>Reset Password</h1>
        <p>Click on this <a href={Link}>Link</a> to reset password</p>

        """

        # emails

        message = create_message(
            recipients= [email],
            subject="Reset Password",
            body=html
        )

        await mail.send_message(message)

        return { "msg": "A reset link has been sent to your email"}
    except Exception as e:
        logging.exception(e)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/reset-password")
async def resetPassword(passwordData:ResetPasswordModel, session: AsyncSession = Depends(session)):
    try:
        result = decodeIdnToken(token=passwordData.token)

        if not result:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="The password reset link has expired")
        
        resp = await auth.updateUserPassword(session=session, email=result, passwordData=passwordData)

        return { "msg": "Password reset successful", "email": result, "user": passwordData, "resp": resp}
    
    except Exception as e:
       raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/refresh")
async def getNewAccessToken(req:Request, resp:Response):
    token = req._cookies.get("refreshToken")

    if token:
        tokenData = decodeToken(token)

        if tokenData is not None and tokenData["refresh"]:
            accessToken = createAccessToken(tokenData["user"], expiry=timedelta(days=0.5))

            resp.set_cookie(
                    key="accessToken",
                    value=accessToken,
                    httponly=True,
                    samesite="lax",
                    path="/",
                    secure=False,  #Todo: set True before deployment
                    max_age=3600,
                    # domain="http://localhost:3000/"
                )
            
            return {"status": "successs"}
        else:
            resp.delete_cookie("refreshToken")
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Please provide a valid refresh token")
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No refresh token found")


@router.get("/profile", response_model= UserModel)
async def getCurrentUser(userDetails = Depends(tokenBearer), session:AsyncSession = Depends(session) ):
    resp =  await auth.getUser(userDetails["user"]["email"], session)
    return resp
    

@router.get("/logout")
async def logout(resp:Response, userDetails = Depends(tokenBearer)):
    # better logout system should be done

   try:
        # await addJtiToBlockList(userDetails["jti"])
            resp.set_cookie(
                key="accessToken",
                value="",
                httponly=True,
                samesite="none",
                path="/",
                secure=True,  #Todo: set True before deployment
                max_age=0,
                # domain="http://localhost:3000/"
            )

            resp.set_cookie(
                key="refreshToken",
                value="",
                httponly=True,
                samesite="none",
                path="/",
                secure=True,  #Todo: set True before deployment
                max_age=0,
                # domain="http://localhost:3000/"
            )
        # res =  await JtiInBlockList(userDetails["jti"])
        
            return { "msg": "Logout successful!"}
   except:
       raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="An error occured")
        
