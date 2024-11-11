import os
from dotenv import load_dotenv
from datetime import timedelta
from passlib.context import CryptContext

# load .env-file
load_dotenv()


class Config:
    # database config
    SQLALCHEMY_DATABASE_URI = os.getenv("RENDER_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # JWT-config
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=240)
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
    JWT_TOKEN_LOCATION = ["headers"]
    JWT_IDENTITY_CLAIM = "user_id"

    # Password-Hashing-context
    pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

    # CORS-config
    CORS_RESOURCES = {r"/*": {"origins": "*"}}
