# from fastapi_mail import FastMail, ConnectionConfig, MessageSchema, MessageType
# from src.config import config
# # from pathlib import Path
# # from typing import List

# # BASE_URL = Path(__file__).resolve().parent

# # TEMPLATE_FOLDER = BASE_URL / "templates"


# mail_config = ConnectionConfig(
#     MAIL_USERNAME = config.MAIL_USERNAME, 
#     MAIL_PASSWORD = config.MAIL_PASSWORD , 
#     MAIL_PORT = config.MAIL_PORT, 
#     MAIL_SERVER = config.MAIL_SERVER, 
#     MAIL_STARTTLS = config.MAIL_STARTTLS, 
#     MAIL_SSL_TLS = config.MAIL_SSL_TLS,  
#     MAIL_FROM = config.MAIL_FROM, 
#     MAIL_FROM_NAME = config.MAIL_FROM_NAME, 
#     VALIDATE_CERTS = config.VALIDATE_CERTS,
#     # TEMPLATE_FOLDER = TEMPLATE_FOLDER, 
# )

# mail = FastMail(
#     config=mail_config
# )

# def create_message(recipients:list[str], subject:str, body:str):
#     message = MessageSchema(
#         recipients=recipients,
#         subject=subject,
#         body=body,
#         subtype=MessageType.html
#     )

#     return message



import json
import base64
from email.mime.text import MIMEText
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from .config import config



def sendMail(to_email:str, resetLink:str):
    tokenInfo = config.GMAIL_TOKEN_DATA

    creds = Credentials.from_authorized_user_info(tokenInfo)

    service =  build("gmail", "v1", credentials=creds)

    message =  MIMEText(
        f"<p>Click <a href={resetLink}>{resetLink}</a> to reset your password</p>",
        "html"
    ) 
    message["to"] = to_email
    message["from"] = "me"
    message["subject"] = "Reset your password"

    raw_message =  base64.urlsafe_b64encode(message.as_bytes()).decode()


    try:
        result  =  service.users().messages().send(userId="me", body={"raw": raw_message}).execute()
        print("successful")

        return result
    except Exception as e:
        print(e)

