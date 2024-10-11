from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "Users"

    user_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    admin = db.Column(db.Boolean, default=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)

    # Relationships
    publishers = db.relationship("Publisher", backref="user", lazy=True)
    authors = db.relationship("Author", backref="user", lazy=True)
    publications = db.relationship("PublicationDetails", backref="user", lazy=True)


class Publisher(db.Model):
    __tablename__ = "Publisher"

    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)
    publisher_name = db.Column(db.String, nullable=False)


class Author(db.Model):
    __tablename__ = "Author"

    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)
    name = db.Column(db.String, nullable=False)
    author_image = db.Column(db.Text)
    birth_date = db.Column(db.Date)


class Book(db.Model):
    __tablename__ = "Book"

    book_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)
    release_date = db.Column(db.String)
    cover_image = db.Column(db.String)
    chapters = db.Column(db.Integer)
    pages = db.Column(db.Integer)

    # Relationships
    publication_details = db.relationship(
        "PublicationDetails", backref="book", lazy=True
    )


class PublicationDetails(db.Model):
    __tablename__ = "Publication_details"

    book_id = db.Column(db.Integer, db.ForeignKey("book.book_id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)
    price = db.Column(db.Numeric)
    country = db.Column(db.String)
    units = db.Column(db.Integer)
    link = db.Column(db.Text)
    language = db.Column(db.String)
