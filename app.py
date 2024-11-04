from flask import (
    Flask,
    request,
    render_template,
    redirect,
    url_for,
    flash,
    session,
    jsonify,
)
from models import Users, db, app, Author, Book, Publisher, Publication_Details
from flask_jwt_extended import (
    JWTManager,
    jwt_required,
    create_access_token,
    create_refresh_token,
    get_jwt_identity,
)
from werkzeug.security import generate_password_hash, check_password_hash
from urllib.parse import urlparse
from urllib.parse import parse_qs
import urllib3
from flasgger import Swagger

app.config["JWT_SECRET_KEY"] = "super-secret"
jwt = JWTManager(app)
swagger = Swagger(app, template_file="swagger.yaml")


# Login Route
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.json.get("email")
        password = request.json.get("password")

    try:
        user = Users.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            # generate jwt token
            access_token = create_access_token(identity=user.user_id)
            return jsonify(access_token=access_token.decode("utf-8"))
        else:
            return {"Invalid email or password"}, 401

    except Exception as e:
        db.session.rollback()
        print(f"Bug during searching for User: {e}")
        return "An error occurred", 500

    return "Please provide your login details."


@app.route("/register", methods=["POST"])
def register():
    try:
        # the clear pw will be hashed
        hashed_password = generate_password_hash(request.json.get("password"))

        # creating user
        create_user = Users(
            first_name=request.json.get("first_name"),
            last_name=request.json.get("last_name"),
            email=request.json.get("email"),
            password=hashed_password,
        )  # the hash pw will be saved here

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
        user = Users.query.get(user_id)

        if not user:
            return jsonify({"message": "User not found"}), 404

        db.session.delete(user)
        db.session.commit()
        print("Test")
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
def show_author():
    """Shows information about the selected author, including picture and books."""
    try:
        author = Author.query.get(author_id)
        if author:
            author_data = {
                "author_id": author.author_id,
                "name": author.name,
                "author_image": author.author_image,
                "birth_date": author.birth_date,
                "books": [
                    {"book_id": book.book_id, "title": book.title}
                    for book in author.books
                ],
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
        author_id = request.json.get("author_id")
        author = Author.query.get(author_id)

        if author:
            author.name = request.json.get("name", author.name)
            author.author_image = request.json.get("author_image", author.author_image)
            author.birth_date = request.json.get("birth_date", author.birth_date)
            db.session.commit()

            updated_author_data = {
                "author_id": author.author_id,
                "name": author.name,
                "author_image": author.author_image,
                "birth_date": author.birth_date,
            }
            return (
                jsonify(
                    {
                        "message": "Author successfully updated",
                        "author": updated_author_data,
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
def get_book_infos():
    """Fetches information about all books."""
    try:
        books_list = [
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
        return jsonify({"books": books_list}), 200

    except Exception as e:
        print(f"Error retrieving books: {e}")
        return jsonify({"message": "An error occurred while retrieving books"}), 500


@app.route("/book", methods=["POST"])
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
def get_publication_details():
    """Shows detailed information about a selected book related to sales, price, etc."""
    print(request.query_string)
    try:
        author_id = request.args.get("author_id")
        book_id = request.args.get("book_id")

        url = "http://127.0.0.1:5000/publication_details?user_id=1&book_id=2"
        parsed_url = urlparse(url)
        user_id = parse_qs(parsed_url.query)["user_id"][0]
        book_id = parse_qs(parsed_url.query)["book_id"][0]

        # search for the publication details based on author_id and book_id
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


@app.route("/book", methods=["DELETE"])
def delete_book():
    """Delete a selected book"""
    try:
        book_id = request.json.get("book_id")
        book = Book.query.get(book_id)

        if book:
            db.session.delete(book)
            db.session.commit()
            return jsonify({"message:" "Book successfully deleted"}), 200
        else:
            return jsonify({"message": "Book not found"}), 404

    except Exception as e:
        db.session.rollback()
        print(f"Error deleting author: {e}")
        return jsonify({"message": "An error occurred while deleting the book"}), 500


if __name__ == "__main__":
    app.run(debug=True)
