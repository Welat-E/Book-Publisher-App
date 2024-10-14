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

    #Relationships between Users and authors, books, publication_details publisher
    authors = db.relationship("Author", backref="user", lazy=True)
    books = db.relationship("Book", backref="user", lazy=True)
    publication_details = db.relationship("PublicationDetails", backref="user", lazy=True)
    publishers = db.relationship("Publisher", backref="user", lazy=True)


class Author(db.Model):
    __tablename__ = "Author"
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
        "PublicationDetails", backref="book", lazy=True
    )


class PublicationDetails(db.Model):
    __tablename__ = "Publication_Details"
    book_id = db.Column(db.Integer, db.ForeignKey("Book.book_id"), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("Users.user_id"))
    price = db.Column(db.Numeric)
    country = db.Column(db.String)
    units = db.Column(db.Integer)
    link = db.Column(db.Text)
    language = db.Column(db.String)


class Publisher(db.Model):
    __tablename__ = "Publisher"
    user_id = db.Column(db.Integer, db.ForeignKey("Users.user_id"), primary_key=True)
    publisher_name = db.Column(db.String)


