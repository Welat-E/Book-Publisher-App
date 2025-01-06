from werkzeug.security import generate_password_hash
from models import Users, Author, Book
from .config import db


def seed_data():
    """Seed initial data into the database."""
    try:
        # Check if the database is empty
        if not Users.query.first():
            print("Seeding initial data...")

            # Add Users
            user1 = Users(
                first_name="Admin",
                last_name="User",
                email="admin@example.com",
                password=generate_password_hash("password"),
                admin=True,
            )
            user2 = Users(
                first_name="John",
                last_name="Doe",
                email="john.doe@example.com",
                password=generate_password_hash("password"),
            )
            db.session.add_all([user1, user2])

            # Add Authors
            author1 = Author(
                name="Jane Austen",
                author_image="https://example.com/jane.jpg",
                birth_date="1775-12-16",
                user_id=1,
            )
            author2 = Author(
                name="Charles Dickens",
                author_image="https://example.com/charles.jpg",
                birth_date="1812-02-07",
                user_id=1,
            )
            db.session.add_all([author1, author2])

            # Add Books
            book1 = Book(
                title="Pride and Prejudice",
                release_date="1813",
                isbn="9780141040349",
                authors_name="Jane Austen",
                author_id=1,
                user_id=1,
            )
            book2 = Book(
                title="Oliver Twist",
                release_date="1837",
                isbn="9780140435226",
                authors_name="Charles Dickens",
                author_id=2,
                user_id=1,
            )
            db.session.add_all([book1, book2])

            db.session.commit()
            print("Data seeded successfully.")
        else:
            print("Data already exists. No seeding performed.")

    except Exception as e:
        db.session.rollback()
        print(f"Error during seeding: {e}")


if __name__ == "__main__":
    from app import app

    with app.app_context():
        seed_data()
