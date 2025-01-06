"""
Configures the Flask app with necessary settings such as database, JWT, CORS, and password hashing.
It uses Singleton patterns for managing app and database instances and integrates 
Swagger for API documentation.
"""
import os
import sys
from datetime import timedelta
from abc import ABCMeta, abstractstaticmethod
from urllib.parse import urlparse, parse_qs
from functools import wraps
from dotenv import load_dotenv
from flask import (
    Flask,
    request,
    jsonify,
    send_file,
    redirect,
    url_for,
    flash,
    render_template,
    session,
)
from flask_jwt_extended import (
    JWTManager,
    jwt_required,
    create_access_token,
    create_refresh_token,
    get_jwt_identity,
)
from passlib.context import CryptContext
from flask_cors import CORS  # a security layer of the browsers
from flasgger import Swagger
from werkzeug.security import generate_password_hash, check_password_hash
from isbnlib import desc, cover, meta
from flask_login import UserMixin
from sqlalchemy.ext.hybrid import hybrid_property
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Date, Numeric, Text
from sqlalchemy.orm import relationship


# Path configs
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, ".."))
sys.path.append(project_root)

# load .env file
load_dotenv()


class Config(metaclass=ABCMeta):
    @abstractstaticmethod
    def getDbInstance():
        """Implement in child class"""

    # database configs
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # JWT-Configs
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=240)
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
    JWT_TOKEN_LOCATION = ["headers"]
    JWT_IDENTITY_CLAIM = "user_id"

    # Password-Hashing-Context
    pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

    # CORS-Config
    CORS_RESOURCES = {r"/*": {"origins": "*"}}


class DbSingleton(Config):
    __db_instance = None

    @staticmethod
    def get_db():
        if DbSingleton.__db_instance is None:
            # we use already the initialized db from config
            DbSingleton.__db_instance = SQLAlchemy()

        return DbSingleton.__db_instance

    @staticmethod
    def getDbInstance():
        return f"Database: {DbSingleton.get_db()}"


class AppSingleton(Config):
    __app_instance = None

    @staticmethod
    def get_app():
        if AppSingleton.__app_instance is None:
            # we use already the initialized db from config
            AppSingleton.__app_instance = Flask(__name__)
        return AppSingleton.__app_instance

    @staticmethod
    def getAppInstance():
        return f"App: {AppSingleton.get_app()}"


app = AppSingleton.get_app()
db = DbSingleton.get_db()
# app.config.from_object(Config)
CORS(app, resources=Config.CORS_RESOURCES)
jwt = JWTManager(app)
app.config.from_object(Config)

db.init_app(app)

# Swagger
base_dir = os.path.abspath(os.path.dirname(__file__))
swagger = Swagger(app, template_file=os.path.join(base_dir, "swagger.yaml"))
