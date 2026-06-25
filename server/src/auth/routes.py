from fastapi import APIRouter, Depends, status, HTTPException, Response, Request
from .schema import UserCreateModel, UserLoginModel, UserModel,EmailsModel
from .services import UserService
from sqlalchemy.ext.asyncio.session  import AsyncSession
from src.db.main import session
from .utilis import createAccessToken, decodeToken, verifyHash
from datetime import timedelta
from src.auth.dependencies import TokenBearer
from src.mail import create_message, mail


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
                samesite="lax",
                path="/",
                secure=False,  #Todo: set True before deployment
                max_age=3600,
                # domain="http://localhost:3000/"
            )

            response.set_cookie(
                key="refreshToken",
                value=refreshToken,
                httponly=True,
                samesite="lax",
                path="/",
                secure=False,  #Todo: set True before deployment
                max_age=3600,
                # domain="http://localhost:3000/"
            )

            
            return { "msg": "Login Successful", "user": user, "accessToken": accessToken}

        elif isValid is False:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Password")
  
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Email")
        


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
        resp.delete_cookie("accessToken")
        resp.delete_cookie("refreshToken")
        # res =  await JtiInBlockList(userDetails["jti"])
        
        return { "msg": "Logout successful!"}
   except:
       raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="An error occured")
        
