from fastapi_mail import FastMail, ConnectionConfig, MessageSchema, MessageType
from src.config import config
from pathlib import Path
# from typing import List

BASE_URL = Path(__file__).resolve().parent

TEMPLATE_FOLDER = BASE_URL / "templates"

if not TEMPLATE_FOLDER.exists():
    TEMPLATE_FOLDER.mkdir(parents=True, exist_ok=True)



mail_config = ConnectionConfig(
    MAIL_USERNAME = config.MAIL_USERNAME, 
    MAIL_PASSWORD = config.MAIL_PASSWORD , 
    MAIL_PORT = config.MAIL_PORT, 
    MAIL_SERVER = config.MAIL_SERVER, 
    MAIL_STARTTLS = config.MAIL_STARTTLS, 
    MAIL_SSL_TLS = config.MAIL_SSL_TLS,  
    MAIL_FROM = config.MAIL_FROM, 
    MAIL_FROM_NAME = config.MAIL_FROM_NAME, 
    VALIDATE_CERTS = config.VALIDATE_CERTS,
    TEMPLATE_FOLDER = TEMPLATE_FOLDER, 
)

mail = FastMail(
    config=mail_config
)

def create_message(recipients:list[str], subject:str, body:str):
    message = MessageSchema(
        recipients=recipients,
        subject=subject,
        body=body,
        subtype=MessageType.html
    )

    return message