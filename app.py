from flask import Flask, request, render_template, redirect, url_for, flash, session
from models import Users, db, app
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
from werkzeug.security import generate_password_hash, check_password_hash

app.config["JWT_SECRET_KEY"] = "super-secret"
jwt = JWTManager(app)


# Login Route
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.get_json().get("email")
        password = request.get_json().get("password")
        print(email)
        try:
            user = Users.query.filter_by(email=email).first()
            print(user)
            if user and check_password_hash(user.password, password):
                print("test")
                #generate jwt token
                access_token = create_access_token(identity=user.user_id)
                
                #transfer it into a string
                access_token_str = str(access_token)
                
                #give token back as json
                return {"access_token": access_token_str}, 200
            else:
                print("Invalid email or password")
                return {"msg": "Invalid details"}, 401

        except Exception as e:
            db.session.rollback()
            print(f"Bug during searching for User: {e}")
            return "An error occurred", 500

    return "Please provide your login details."



# No html for now, use Postman for checking everything.


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        try:
            # the clear pw will be hashed
            hashed_password = generate_password_hash(request.form.get("password"))

            # creating user
            create_user = Users(
                first_name=request.form.get("first_name"),
                last_name=request.form.get("last_name"),
                admin=False,
                email=request.form.get("email"),
                password=hashed_password,  # the hash pw will be saved here
            )

            # add user in database
            db.session.add(create_user)
            db.session.commit()
            return "Successfully registered!"

        except Exception as e:
            db.session.rollback()
            print(f"Bug during creating User: {e}")
            return "An error occurred during registration"

    return "Please fill the registration form."


@app.route("/get_users", methods=["GET"])
@jwt_required()
def get_users():
    users = Users.query.all()
    return render_template("users.html", users=users)


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
