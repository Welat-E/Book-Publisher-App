from flask_sqlalchemy import SQLAlchemy

# Initialize the db instance from Flask-SQLAlchemy

db = SQLAlchemy()


class Users(db.Model):
    """
    Represents a User in the database.
    """

    __tablename__ = "Users"
    user_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    role = db.Column(db.String(5))
    email = db.Column(db.String)
    password = db.Column(db.String)

    # Define a relationship between User and  Author and Publisher
    publisher = db.relationship("Publisher", backref="users", lazy=True)
    author = db.relationship("Author", backref="users", lazy=True)

    def __repr__(self):
        return f"<User {self.first_name}>"


class Publisher(db.Model):
    """
    Represents a Publisher in the database.
    """

    __tablename__ = "Publisher"
    user_id = db.Column(db.Integer)
    publisher_name = db.Column(dn.String)

    # Relationship between Publisher and Publication_Details
    publication_details = db.relationship(
        "Publication_Details", backref="publisher", lazy=True
    )

    def __repr__(self):
        return f"<Publisher {self.publisher_name}>"


class Publication_Details(db.Model):
    """
    Represents Publication_Details in the database.
    """

    __tablename__ = "Publication_Details"
    user_id = db.Column(db.Integer)
    book_id = db.Column(db.Integer)
    price = db.Column(db.Integer)
    country = db.Column(db.String)
    units = db.Column(db.Integer)
    release_date = db.Column(db.String)
    cover_image = db.Column(db.String)
    pages = db.Column(db.Integer)
    chapters = db.Column(db.Integer)
    Link = db.Column(db.String)

    #Relationship between Publication_Details and Author and Book
    author = db.relationship("Author", backref="Publication_Details", lazy=True)
    book = db.relationship("Book", backref="Publication_Details", lazy=True)


class Author(db.Model):
    """
    Represents Authors in the database.
    """

    __tablename__ = "Author"
    user_id = db.Column(db.Integer)
    book_id = db.Column(db.Integer)
    image_cover = db.Column(db.String)
    birth_date = db.Column(db.String)

    #Relationship between Author and Book
    book = db.relationship("Book", backref="Author", lazy=True)


