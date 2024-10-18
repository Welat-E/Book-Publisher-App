from flask import Flask, request, render_template, redirect, url_for, flash, session
from models import Users, Publisher, Book, Author, PublicationDetails
from flask_jwt_extended import JWTManager

app = Flask(__name__)
jwt = JWTManager(app)


@app.route("/", methods=["GET", "POST"])
def login():
    """Shows Login Page with name and password and a function where you can
    make forgot password"""
    return "Hello, world!"


@app.route("/register", methods=["POST"])
def register():
    first_user = Users(
        first_name="publisher",
        last_name="company",
        admin=True,
        email="publisher1@bookapp.com",
        password="publisher123",
    )
    return"Success!"
    # Insert user into the database
    # try:
    #     db.session.add(first_user)
    #     db.session.commit()
    #     print("User successfully created.")
    # except Exception as e:
    #     db.session.rollback()
    #     print(f"Bug during creating User: {e}")


@app.route("/dashboard")
def dashboard():
    if not current_user.is_authenticated or not current_user.admin:
        return redirect(url_for("login"))
    return render_template("admin_dashboard.html")


@app.route("/dashboard/author/<int:id>", methods=["GET", "POST"])
def author():
    """Shows informations about the selected author, a pic and their books,
    which you can edit, add, delete etc."""
    pass


@app.route("/dashboard/add_author", methods=["POST"])
def add_author():
    """Add Author path"""
    # add author path from the database
    pass


@app.route("/dashboard/delete_author", methods=["POST"])
def delete_author():
    """Delete Author path"""
    pass


@app.route("/dashboard/edit_author", methods=["POST"])
def edit_author():
    """Edit author"""
    pass


@app.route("/dashboard/author/<int:id>/books", methods=["GET", "POST"])
def books():
    """Here you can add, delete, edit, and view information about the books,
    how much they have been sold, the price, etc."""
    pass


@app.route("/dashboard/author/<int:id>/books/add_book", methods=["POST"])
def add_book():
    """Add books from the selected author"""
    pass


@app.route("/dashboard/author/<int:author_id>/books/<int:book_id>", methods=["GET"])
def book_detail(author_id, book_id):
    """Shows detailed information about a selected book"""
    pass


@app.route(
    "/dashboard/author/<int:author_id>/books/<int:book_id>/edit", methods=["POST"]
)
def edit_selected_book(author_id, book_id):
    """Edit a selected book"""
    pass


@app.route(
    "/dashboard/author/<int:author_id>/books/<int:book_id>/delete", methods=["POST"]
)
def delete_selected_book(author_id, book_id):
    """Delete a selected book"""
    pass


if __name__ == "__main__":
    app.run(debug=True)
