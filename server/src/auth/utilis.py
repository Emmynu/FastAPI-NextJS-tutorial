from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from datetime import timedelta, datetime
import jwt
from src.config import config
import uuid
import logging
from itsdangerous import URLSafeTimedSerializer

ph = PasswordHasher()
ACCESS_TOKEN_EXPIRY = 3600

def generatePasswordHash(password:str) -> str:
   hash =  ph.hash(password)

   return hash


def verifyHash(password:str, hash:str) :
    try:
        verifiedPassword = ph.verify(hash, password)

        return verifiedPassword
    
    except VerifyMismatchError :
        return False
       


def createAccessToken(data:dict, expiry:timedelta  , refresh:bool = False):
    
    payload = {}

    payload["user"] =  data
    payload["exp"] =  datetime.now() + expiry
    payload["jti"] = str(uuid.uuid4())

    payload["refresh"] = refresh

    token = jwt.encode(
        payload=payload,
        key=config.JWT_SECRET,
        algorithm=config.JWT_ALGORITHM
    )

    return token



def decodeToken(token:str) -> dict:
    try:
        tokenData = jwt.decode(
            jwt=token,
            key=config.JWT_SECRET,
            algorithms=[config.JWT_ALGORITHM]
        )

        return tokenData
    
    except jwt.PyJWTError as e:
        logging.exception(e)
        return None
    
serializer = URLSafeTimedSerializer(secret_key=config.JWT_SECRET, salt="idnToken")


def createIdnToken(data):
    return serializer.dumps(data)


def decodeIdnToken(token):
    return serializer.loads(token, max_age=900, salt="idnToken")