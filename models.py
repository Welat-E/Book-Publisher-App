from flask import Flask
from flask_login import UserMixin
from sqlalchemy.ext.hybrid import hybrid_property
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv
from passlib.context import CryptContext
from datetime import timedelta
from flask_cors import CORS

load_dotenv()

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://127.0.0.1:5000"}})

# PostgreSQL config.
# database_url = os.getenv("DATABASE_URL")
render_url = os.getenv("RENDER_URL")
app.config["SQLALCHEMY_DATABASE_URI"] = render_url  # database_url (before)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=240)  # Access-Token expires
# app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=1) #TODO Refresh-Token after 1 day #
JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY")
JWT_TOKEN_LOCATION = ["headers"]
JWT_IDENTITY_CLAIM = "user_id"


pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

# starting database
db = SQLAlchemy(app)


class Users(db.Model, UserMixin):

    __tablename__ = "Users"
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    admin = db.Column(db.Boolean, default=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column("password", db.String, nullable=False)

    authors = db.relationship("Author", backref="user", lazy=True)
    books = db.relationship("Book", backref="user", lazy=True)
    publication_details = db.relationship(
        "Publication_Details", backref="user", lazy=True
    )
    publishers = db.relationship("Publisher", backref="user", lazy=True)

    # def __init__(self, first_name, last_name):
    #     self.first_name = first_name
    #     self.last_name = last_name


class Author(db.Model):
    __tablename__ = "Author"
    author_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    author_image = db.Column(db.Text)
    birth_date = db.Column(db.Date)
    user_id = db.Column(db.Integer, db.ForeignKey("Users.user_id"))


class Book(db.Model):
    __tablename__ = "Book"
    book_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("Users.user_id"))
    release_date = db.Column(db.String)
    cover_image = db.Column(db.String)
    chapters = db.Column(db.Integer)
    pages = db.Column(db.Integer)

    publication_details = db.relationship(
        "Publication_Details", backref="book", lazy=True
    )


class Publication_Details(db.Model):
    __tablename__ = "Publication_Details"
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey("Book.book_id"))
    user_id = db.Column(db.Integer, db.ForeignKey("Users.user_id"))
    price = db.Column(db.Numeric)
    country = db.Column(db.String)
    units = db.Column(db.Integer)
    link = db.Column(db.Text)
    language = db.Column(db.String)


class Publisher(db.Model):
    __tablename__ = "Publisher"
    publisher_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("Users.user_id"))
    publisher_name = db.Column(db.String)


#  create database
# with app.app_context():
#     db.create_all()

print("Loaded DATABASE URI:", os.getenv("RENDER_URL"))
