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
    publishers = db.relationship("Publisher", backref="users", lazy=True)
    authors = db.relationship("Author", backref="users", lazy=True)

    def __repr__(self):
        return f"<User {self.first_name}>"
