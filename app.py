from models.models import Users, Book, Publication_Details, Author
from config.config import *


def is_admin():
    user_id = get_jwt_identity()
    user = Users.query.get(user_id)
    if user:
        print(f"User ID: {user_id}, Admin: {user.admin}")
    return user and user.admin


def admin_required(fn):
    @wraps(fn)
    @jwt_required()  # Ensure authentication
    def wrapper(*args, **kwargs):
        user_id = get_jwt_identity()
        user = Users.query.get(user_id)  # get user from database
        if not user or not user.admin:  # check if you have admin permission
            return jsonify({"msg": "Admin access required"}), 403
        return fn(*args, **kwargs)

    return wrapper


# Login Route
@app.route("/login", methods=["POST"])
def login():
    if request.method == "POST":
        email = request.json.get("email")
        password = request.json.get("password")

    try:
        user = Users.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            access_token = create_access_token(identity=str(user.user_id))

            return jsonify(
                {
                    "access_token": access_token,
                    "message": "User successfully logged in.",
                }
            )
        else:
            return jsonify({"message": "Invalid email or password"}), 401

    except Exception as e:
        db.session.rollback()
        print(f"Bug during searching for User: {e}")
        return jsonify({"message": "An error occurred"}), 500

    return jsonify({"message": "Please provide your login details"}), 400


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

        # Return user details after successful registration
        return (
            jsonify(
                {
                    "message": "User successfully registered.",
                    "user": {
                        "first_name": create_user.first_name,
                        "last_name": create_user.last_name,
                        "email": create_user.email,
                    },
                }
            ),
            200,
        )

    except Exception as e:
        db.session.rollback()
        print(f"Bug during creating User: {e}")
        return jsonify({"message": "An error occurred during registration"}), 500


@app.route("/users", methods=["GET"])
@admin_required
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
    """Allows a user or an admin to delete a user account."""
    try:
        current_user_id = int(
            get_jwt_identity()
        )  # ID from logged in Users from the JWT
        user_to_delete = Users.query.get(user_id)
        if not user_to_delete:
            return jsonify({"message": "User not found"}), 404

        # Check whether the logged in user is an admin or wants to delete themselves
        if not (current_user_id == user_to_delete.user_id or is_admin()):
            return jsonify({"message": "Permission denied"}), 403

        db.session.delete(user_to_delete)
        db.session.commit()
        return jsonify({"message": "User and related data successfully deleted"}), 200

    except Exception as e:
        db.session.rollback()
        print(f"Error deleting user: {e}")
        return jsonify({"message": "An error occurred while deleting the user"}), 500


@app.route("/author", methods=["GET"])
@admin_required
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
        user_id = int(get_jwt_identity())
        name = request.json.get("name")
        author = Author.query.filter_by(name=name).first()
        if author:
            return "The Author already exists in the database"

        new_author = Author(
            user_id=user_id,
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
                    "user_id": new_author.user_id,
                    "author_id": new_author.author_id,
                }
            ),
            200,
        )

    except Exception as e:
        db.session.rollback()
        print(f"Error during author creation: {e}")
        return "An error occurred during author creation."


@app.route("/author/<int:id>", methods=["GET"])
@jwt_required()
def show_author(id):
    """Shows information about the selected author, including picture and books."""
    try:
        author = Author.query.get(id)
        if author:
            author_data = {
                "author_id": author.author_id,
                "name": author.name,
                "author_image": author.author_image,
                "birth_date": str(author.birth_date) if author.birth_date else None,
                "books": [
                    {
                        "book_id": book.book_id,
                        "user_id": book.user_id,
                        "author_id": book.author_id,
                        "title": book.title,
                        "release_date": book.release_date,
                        "isbn": book.isbn,
                        "authors_name": book.authors_name,
                    }
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
@admin_required
def edit_author():
    """Edit author details."""
    try:
        author_id = request.json.get("author_id")  # saving user input in a variable as
        author = Author.query.get(author_id)  # searching the author in the database

        if author:  # if author found can we change all the things about author
            author.name = request.json.get("name", author.name)
            author.author_image = request.json.get("author_image", author.author_image)
            author.birth_date = request.json.get("birth_date", author.birth_date)
            db.session.commit()  # saving the changes

            updated_author_data = {  # saving new data into updated_author_data
                "author_id": author.author_id,
                "name": author.name,
                "author_image": author.author_image,
                "birth_date": author.birth_date,
            }
            return (
                jsonify(
                    {
                        "message": "Author successfully updated",
                        "author": updated_author_data,  # showing new author data as return
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
@admin_required
def get_book_infos():
    """Fetches information about all books."""
    try:
        books_list = [  # for each book in the book table, we create an entry as a dictionary with the data,
            # and preparing it for a json response
            {
                "author_id": new_book.author_id,
                "title": new_book.title,
                "release_date": new_book.release_date,
                "isbn": new_book.isbn,
                "authors_name": new_book.authors_name,
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
        user_id = int(get_jwt_identity())
        author_id = request.json.get("author_id")
        isbn = request.json.get("isbn")
        meta_data = meta(isbn, service="openl")  # Fetch data using isbnlib

        if not meta_data:
            return jsonify({"message": "Invalid ISBN provided."}), 400

        new_book = Book(
            user_id=user_id,
            author_id=author_id,
            title=meta_data.get("Title"),
            release_date=meta_data.get("Year"),
            isbn=isbn,
            authors_name=", ".join(meta_data.get("Authors", [])),
        )
        db.session.add(new_book)
        db.session.commit()
        print(f"Meta data fetched: {meta_data}")

        # json response
        return (
            jsonify(
                {
                    "message": "Book successfully added",
                    "book": {
                        "book_id": new_book.book_id,
                        "user_id": new_book.user_id,
                        "author_id": new_book.author_id,
                        "title": new_book.title,
                        "release_date": new_book.release_date,
                        "isbn": new_book.isbn,
                        "authors_name": new_book.authors_name,
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
@jwt_required()
def edit_book(book_id):
    """Edit a selected book based on book_id."""
    try:
        # recall Book by book_id
        book = Book.query.get(book_id)

        if book:
            book.release_date = request.json.get("release_date", book.release_date)
            book.title = request.json.get("title", book.title)
            book.release_date = request.json.get("release_date", book.release_date)
            book.isbn = request.json.get("isbn", book.isbn)
            book.authors_name = request.json.get("authors_name", book.authors_name)

            db.session.commit()

            updated_book_data = {
                "book_id": new_book.book_id,
                "user_id": new_book.user_id,
                "author_id": new_book.author_id,
                "title": new_book.title,
                "release_date": new_book.release_date,
                "isbn": new_book.isbn,
                "authors_name": new_book.authors_name,
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
@admin_required
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
