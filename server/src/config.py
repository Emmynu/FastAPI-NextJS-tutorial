from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

# to get the DBURL from the env file
class Settings(BaseSettings):
    DATABASE_URL:str
    JWT_SECRET:str
    JWT_ALGORITHM:str
    REDIS_HOST:str = "localhost"
    REDIS_PORT:int = 6379
    MAIL_USERNAME: str 
    MAIL_PASSWORD: str 
    MAIL_PORT: int = 465
    MAIL_SERVER: str 
    MAIL_STARTTLS: bool = False
    MAIL_SSL_TLS: bool  =  True
    MAIL_FROM: str 
    MAIL_FROM_NAME: str
    USE_CREDENTIALS:bool =  True
    VALIDATE_CERTS: bool = True
    GMAIL_TOKEN_DATA: Optional[dict] = None




    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )


config = Settings()