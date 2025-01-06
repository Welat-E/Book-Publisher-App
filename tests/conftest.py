import sys
import os

# Add the project root directory to sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, ".."))
sys.path.append(project_root)

import pytest
from app import app as flask_app
from config.config import db


@pytest.fixture
def test_app():
    flask_app.config["TESTING"] = True
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
        "DATABASE_URL",
        "postgresql://postgres:postgres@localhost:5432/publisher_book_app",
    )
    yield flask_app


@pytest.fixture
def client(test_app):
    with test_app.test_client() as client:
        with test_app.app_context():
            db.create_all()  # Tabellen erstellen
        yield client
        with test_app.app_context():
            db.session.remove()
            db.drop_all()
