from flask import Flask, request, render_template

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/", methods=["GET"])
def login():
    """Shows Login Page with name and password and a function where you can
    make forgot password"""
    return "Hello, world!"


@app.route("/register", methods=["POST"])
def register():
    """Registration form for User"""
    pass


@app.route("/forget_password", methods=["POST"])
def forgot_password():
    """Function to reset password when User forgot"""
    pass


@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    """Shows the different Authors who are in the Publication Company"""
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


@app.route("/dashboard/author/<int:id>", methods=["GET", "POST"])
def author():
    """Shows informations about the selected author, a pic and their books,
    which you can edit, add, delete etc."""
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


@app.run