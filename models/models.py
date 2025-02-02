import sys
import os

# Add the project root directory to sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, ".."))
sys.path.append(project_root)

from config.config import *


class Users(db.Model, UserMixin):
    __tablename__ = "Users"
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    admin = db.Column(db.Boolean, default=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column("password", db.String, nullable=False)

    authors = db.relationship(
        "Author", back_populates="user", lazy=True, cascade="all, delete-orphan"
    )
    books = db.relationship(
        "Book", back_populates="user", lazy=True, cascade="all, delete-orphan"
    )
    publishers = db.relationship("Publisher", back_populates="user", lazy=True)


class Author(db.Model):
    __tablename__ = "Author"
    author_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    author_image = db.Column(db.Text)
    birth_date = db.Column(db.Date)
    user_id = db.Column(db.Integer, db.ForeignKey("Users.user_id"))

    user = db.relationship("Users", back_populates="authors")
    publication_details = db.relationship(
        "Publication_Details", back_populates="author", lazy=True
    )
    books = db.relationship("Book", back_populates="author", lazy=True)


class Book(db.Model):
    __tablename__ = "Book"
    book_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("Users.user_id"))
    author_id = db.Column(db.Integer, db.ForeignKey("Author.author_id"))
    title = db.Column(db.String)
    release_date = db.Column(db.String)
    isbn = db.Column(db.String)
    authors_name = db.Column(db.String)

    user = db.relationship("Users", back_populates="books")
    author = db.relationship("Author", back_populates="books")
    publication_details = db.relationship(
        "Publication_Details", back_populates="book", lazy=True
    )


class Publication_Details(db.Model):
    __tablename__ = "Publication_Details"
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey("Book.book_id"))
    author_id = db.Column(db.Integer, db.ForeignKey("Author.author_id"))
    price = db.Column(db.Numeric)
    country = db.Column(db.String)
    units = db.Column(db.Integer)
    link = db.Column(db.Text)
    language = db.Column(db.String)

    book = db.relationship("Book", back_populates="publication_details")
    author = db.relationship("Author", back_populates="publication_details")


class Publisher(db.Model):
    __tablename__ = "Publisher"
    publisher_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("Users.user_id"))
    publisher_name = db.Column(db.String)

    user = db.relationship("Users", back_populates="publishers")


# create database

with app.app_context():
    db.create_all()
