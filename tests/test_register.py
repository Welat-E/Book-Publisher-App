import sys
import os
import json
import pytest

# Add the project root directory to sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, ".."))
sys.path.append(project_root)

from models.models import Users
from werkzeug.security import generate_password_hash
from app import app, db


def test_index(client):
    """Test if the /register route is reachable via POST."""
    response = client.post("/register")
    assert response.status_code in [
        200,
        500,
    ], f"Unexpected status code: {response.status_code}"


def test_register_endpoint(client):
    """Test the /register endpoint."""
    response = client.post(
        "/register",
        data=json.dumps(
            {
                "first_name": "Publisher",
                "last_name": "Bookapp",
                "email": "publisher@bookapp.com",
                "password": "password2",
            }
        ),
        content_type="application/json",
    )
    assert response.status_code == 200
    data = response.get_json()
    assert data["message"] == "User successfully registered."


# def test_register_page(app, client):
#     res = client.post("/login")
#     assert res.status_code == 200
def test_login_endpoint(client):
    """Test the /login endpoint."""
    # Register a user first
    client.post(
        "/register",
        data=json.dumps(
            {
                "first_name": "Publisher",
                "last_name": "Bookapp",
                "email": "publisher@bookapp.com",
                "password": "password2",
            }
        ),
        content_type="application/json",
    )

    # Test valid login
    response = client.post(
        "/login",
        data=json.dumps(
            {
                "email": "publisher@bookapp.com",
                "password": "password2",
            }
        ),
        content_type="application/json",
    )
    assert (
        response.status_code == 200
    ), f"Unexpected status code: {response.status_code}"
    data = response.get_json()
    assert data["message"] == "User successfully logged in."
    assert "access_token" in data, "JWT token missing in response"


@pytest.fixture
def create_admin_user():
    """Fixture to create an admin user."""
    with app.app_context():
        admin_user = Users(
            first_name="Admin",
            last_name="User",
            email="adminuser@example.com",
            password=generate_password_hash("password2"),
            admin=True,
        )
        db.session.add(admin_user)
        db.session.commit()
        print(f"Admin user created with email: {admin_user.email}")
    return admin_user


def test_get_users(client, create_admin_user):
    """Test the /users endpoint for admin users."""
    # Login as admin user (in this case manually simulated)
    response = client.post(
        "/login",
        data=json.dumps(
            {
                "email": "adminuser@example.com",
                "password": "password2",
            }
        ),
        content_type="application/json",
    )
    print(response.data)

    #take the token from the response
    data = response.get_json()
    token = data.get("access_token")

    #check if token is available
    assert token, "Token is missing in response"

    # Test access to /users with an admin token
    response = client.get(
        "/users",
        headers={"Authorization": f"Bearer {token}"},
    )

    # Check the status code and response data
    assert (
        response.status_code == 200
    ), f"Unexpected status code: {response.status_code}"
    data = response.get_json()
    assert "users" in data, "Users key missing in response"
    assert len(data["users"]) > 0, "No users found"
    assert (
        data["users"][0]["email"] == "adminuser@example.com"
    ), "Admin user not in list"


# def test_admin_user_creation(create_admin_user):
#     """Test admin user creation and print email."""
#     admin_user = create_admin_user
#     print(f"Admin user email: {admin_user.email if admin_user else 'Not Found'}")
#     assert admin_user.email == "adminuser@example.com"
