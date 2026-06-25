import redis.asyncio as redis
from src.config import config


JTI_TOKEN_EXPIRY = 3600

redisTokenBlockList = redis.Redis(
    host=config.REDIS_HOST,
    port=config.REDIS_PORT,
    decode_responses=True
)


async def addJtiToBlockList(jti):
    await redisTokenBlockList.ping()
    print("REDIS CONN")
    await redisTokenBlockList.setex(
        name=jti,
        value="blocked",
        time=JTI_TOKEN_EXPIRY
    )
    # return
    


async def JtiInBlockList(jti:str):
    jti = await redisTokenBlockList.get(jti)

    return jti
    
    # return True if jti is not None else False
