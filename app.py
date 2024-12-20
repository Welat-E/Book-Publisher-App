import os
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

from flask_cors import CORS  # a security layer of the browsers
from flasgger import Swagger
from models.models import Users, db, Author, Book, Publisher, Publication_Details
from werkzeug.security import generate_password_hash, check_password_hash
from urllib.parse import urlparse, parse_qs
from config.config import Config

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)  # initialise the database
CORS(app, resources=Config.CORS_RESOURCES)
jwt = JWTManager(app)

base_dir = os.path.abspath(os.path.dirname(__file__))
swagger = Swagger(app, template_file=os.path.join(base_dir, "config", "swagger.yaml"))


# Login Route
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.json.get("email") #we save the email, pw what we typed in swagger in variables
        password = request.json.get("password")

    try:
        user = Users.query.filter_by(email=email).first() #it searches for the first email in the db that matches with the variable

        if user and check_password_hash(user.password, password):
            access_token = create_access_token(identity=user.user_id)#generate jwt token if email and pw was correct like in db
            return jsonify(access_token=access_token) #returns the token
        else:
            return {"Invalid email or password.."}, 401 #unauthorized


    except Exception as e:
        db.session.rollback()
        print(f"Bug during searching for User: {e}")
        return "An error occurred", 500

    return "Please provide your login details."


@app.route("/register", methods=["POST"])
def register():
    try:
        # the clear password will be hashed
        hashed_password = generate_password_hash(request.json.get("password"))

        # creating user
        create_user = Users(
            first_name=request.json.get("first_name"),
            last_name=request.json.get("last_name"),
            email=request.json.get("email"),
            password=hashed_password,  # the hashed password will be saved here
        )

        db.session.add(create_user)
        db.session.commit()

        return (
            jsonify(
                {
                    "first_name": create_user.first_name,
                    "last_name": create_user.last_name,
                    "email": create_user.email,
                }
            ),
            200,
        )

    except Exception as e:
        db.session.rollback()
        print(f"Bug during creating User: {e}")
    return "An error occurred during registration"


@app.route("/users", methods=["GET"])
@jwt_required()
def get_users():
    # Fetch all users and convert to list of dicts in one step
    users_list = [
        {
            "user_id": user.user_id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "admin": user.admin,
        }
        for user in Users.query.all()
    ]

    return jsonify({"users": users_list}), 200


@app.route("/users/<int:user_id>", methods=["DELETE"])
@jwt_required()
def delete_user(user_id):
    """Deletes a user from the database."""
    try:
        current_user_id = get_jwt_identity()
        current_user = Users.query.get(current_user_id)

        if not current_user or not current_user.admin:
            return jsonify({"message": "Only admins can delete users"}), 403

        user = Users.query.get(user_id)
        if not user:
            return jsonify({"message": "User not found"}), 404

        db.session.delete(user)
        db.session.commit()
        return jsonify({"message": "User successfully deleted"}), 200

    except Exception as e:
        db.session.rollback()
        print(f"Error deleting user: {e}")
        return jsonify({"message": "An error occurred while deleting the user"}), 500



@app.route("/author", methods=["GET"])
@jwt_required()
def get_authors():
    try:
        authors_list = [
            {
                "author_id": author.author_id,
                "name": author.name,
                "author_image": author.author_image,
                "birth_date": author.birth_date,
            }
            for author in Author.query.all()
        ]
        return jsonify({"author": authors_list}), 200

    except Exception as e:
        print(e)
        return jsonify({"message": "An error occurred while retrieving authors"}), 500


@app.route("/author", methods=["POST"])
@jwt_required()
def create_author():
    try:
        name = request.json.get("name")
        author = Author.query.filter_by(name=name).first()
        if author:
            return "The Author already exists in the database"

        new_author = Author(
            name=name,
            author_image=request.json.get("author_image"),
            birth_date=request.json.get("birth_date"),
        )
        db.session.add(new_author)
        db.session.commit()

        # give all relevant fields back
        return (
            jsonify(
                {
                    "message": "Author successfully created",
                    "name": new_author.name,
                    "author_image": new_author.author_image,
                    "birth_date": new_author.birth_date,
                }
            ),
            200,
        )

    except Exception as e:
        db.session.rollback()
        print(f"Error during author creation: {e}")
        return "An error occurred during author creation."


@app.route("/author/<int:id>", methods=["GET"])
def show_author(id):
    """Shows information about the selected author, including picture and books."""
    try:
        author = Author.query.get(id)
        if author:
            author_data = {
                "author_id": author.author_id,
                "name": author.name,
                "author_image": author.author_image,
                "birth_date": author.birth_date,
                # "books": [
                #     {"book_id": book.book_id, "title": book.title}
                #     for book in author.books
                # ],
            }
            return jsonify(author_data), 200
        else:
            return jsonify({"message": "Author not found"}), 404

    except Exception as e:
        print(f"Error retrieving author: {e}")
        return (
            jsonify({"message": "An error occurred while retrieving the author"}),
            500,
        )


@app.route("/author", methods=["PUT"])
@jwt_required()
def edit_author():
    """Edit author details."""
    try:
        author_id = request.json.get("author_id") #saving user input in a variable as
        author = Author.query.get(author_id) #searching the author in the database 

        if author: #if author found can we change all the things about author
            author.name = request.json.get("name", author.name)
            author.author_image = request.json.get("author_image", author.author_image)
            author.birth_date = request.json.get("birth_date", author.birth_date)
            db.session.commit() #saving the changes

            updated_author_data = {  #saving new data into updated_author_data
                "author_id": author.author_id,
                "name": author.name,
                "author_image": author.author_image,
                "birth_date": author.birth_date,
            }
            return (
                jsonify(
                    {
                        "message": "Author successfully updated",
                        "author": updated_author_data, #showing new author data as return
                    }
                ),
                200,
            )

        else:
            return jsonify({"message": "Author not found"}), 404

    except Exception as e:
        db.session.rollback()
        print(f"Error updating author: {e}")
        return jsonify({"message": "An error occurred while updating the author"}), 500


@app.route("/book", methods=["GET"])
@jwt_required()
def get_book_infos():
    """Fetches information about all books."""
    try:
        books_list = [   #for each book in the book table, we create an entry as a dictionary with the data, 
                         #and preparing it for a json response

            {
                "book_id": book.book_id,
                "user_id": book.user_id,
                "release_date": book.release_date,
                "cover_image": book.cover_image,
                "chapters": book.chapters,
                "pages": book.pages,
            }
            for book in Book.query.all()
        ]
        return jsonify({"Here are all books in your database:": books_list}), 200

    except Exception as e:
        print(f"Error retrieving books: {e}")
        return jsonify({"message": "An error occurred while retrieving books"}), 500


@app.route("/book", methods=["POST"])
@jwt_required()
def add_book():
    """Add a new book for a selected author."""
    try:
        # retrieve values from the request
        user_id = request.json.get("user_id")
        release_date = request.json.get("release_date")
        cover_image = request.json.get("cover_image")
        chapters = request.json.get("chapters")
        pages = request.json.get("pages")

        new_book = Book(
            user_id=user_id,
            release_date=release_date,
            cover_image=cover_image,
            chapters=chapters,
            pages=pages,
        )
        db.session.add(new_book)
        db.session.commit()

        return (
            jsonify(
                {
                    "message": "Book successfully added",
                    "book": {
                        "book_id": new_book.book_id,
                        "user_id": new_book.user_id,
                        "release_date": new_book.release_date,
                        "cover_image": new_book.cover_image,
                        "chapters": new_book.chapters,
                        "pages": new_book.pages,
                    },
                }
            ),
            201,
        )

    except Exception as e:
        db.session.rollback()
        print(f"Error adding book: {e}")
        return jsonify({"message": "An error occurred while adding the book"}), 500


@app.route("/book/<int:book_id>", methods=["PUT"])
def edit_book(book_id):
    """Edit a selected book based on book_id."""
    try:
        # recall Book by book_id
        book = Book.query.get(book_id)

        if book:
            book.release_date = request.json.get("release_date", book.release_date)
            book.cover_image = request.json.get("cover_image", book.cover_image)
            book.chapters = request.json.get("chapters", book.chapters)
            book.pages = request.json.get("pages", book.pages)

            db.session.commit()

            updated_book_data = {
                "book_id": book.book_id,
                "release_date": book.release_date,
                "cover_image": book.cover_image,
                "chapters": book.chapters,
                "pages": book.pages,
            }
            return (
                jsonify(
                    {"message": "Book successfully updated", "book": updated_book_data}
                ),
                200,
            )
        else:
            return jsonify({"message": "Book not found"}), 404

    except Exception as e:
        db.session.rollback()
        print(f"Error updating book: {e}")
        return jsonify({"message": "An error occurred while updating the book"}), 500


@app.route("/publication_details", methods=["GET"])
@jwt_required()
def get_publication_details():
    """Shows detailed information about a selected book related to sales, price, etc."""
    print(request.query_string)
    try:
        # take the parameters from the query request
        user_id = request.args.get("user_id")
        book_id = request.args.get("book_id")

        if not book_id:
            return jsonify({"message": "book_id is required"}), 400

        publication_details = Publication_Details.query.filter_by(
            user_id=user_id, book_id=book_id
        ).first()

        if publication_details:
            details_data = {
                "id": publication_details.id,
                "book_id": publication_details.book_id,
                "user_id": publication_details.user_id,
                "price": publication_details.price,
                "country": publication_details.country,
                "units": publication_details.units,
                "link": publication_details.link,
                "language": publication_details.language,
            }
            return jsonify(details_data), 200
        else:
            return jsonify({"message": "Publication details not found"}), 404
    except Exception as e:
        print(f"Error retrieving publication details: {e}")
        return (
            jsonify(
                {"message": "An error occurred while retrieving publication details"}
            ),
            500,
        )


@app.route("/book/<int:book_id>", methods=["DELETE"])
@jwt_required()
def delete_book(book_id):
    """Delete a selected book"""
    try:
        # searching for the book through id
        book = Book.query.get(book_id)

        if not book:
            return jsonify({"message": "Book not found"}), 404

        db.session.delete(book)
        db.session.commit()
        return jsonify({"message": "Book successfully deleted"}), 200

    except Exception as e:
        db.session.rollback()
        print(f"Error deleting book: {e}")
        return jsonify({"message": "An error occurred while deleting the book"}), 500


if __name__ == "__main__":
    app.run(debug=True)
