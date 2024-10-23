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
from models import Users, db, app
from flask_jwt_extended import (
    JWTManager,
    jwt_required,
    create_access_token,
    create_refresh_token,
    get_jwt_identity,
)
from werkzeug.security import generate_password_hash, check_password_hash

app.config["JWT_SECRET_KEY"] = "super-secret"
jwt = JWTManager(app)


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


@app.route("/get_users", methods=["GET"])
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


@app.route("/dashboard")
@jwt_required()
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
