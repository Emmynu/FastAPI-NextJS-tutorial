from fastapi.security import HTTPBearer
from fastapi.requests import Request
from .utilis import decodeToken
from fastapi import HTTPException, status, Depends
from src.db.redis import JtiInBlockList

class TokenBearer(HTTPBearer):
    def __init__(self,  auto_error = True):
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request):

        token = None

        headers =  request.headers.get("Authorization", "").lower()
      
        if headers:
            try:
                creds = await super().__call__(request)
                token = creds.credentials
            except:
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Please provide a valid access token")

        else:
            token = request.cookies.get("accessToken")

            if not token :
                raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Please provide a valid access token")
            
    
        isTokenValid =  self.validateToken(token)

        if isTokenValid:
            tknData =  decodeToken(token)

            # tokenInBlockList  = await JtiInBlockList(tknData["jti"])

            # if tokenInBlockList:
            #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail={
            #         "error": "Invalid Token",
            #         "resolution": "Go back to the login page"
            #     })
            
            if tknData is not None and tknData["refresh"]:
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Please provide a valid access token")

            return tknData
        else:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")

    def validateToken(self, token):
        tkn =  decodeToken(token)

        return True if tkn is not None else False 

