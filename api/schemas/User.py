from marshmallow import Schema, fields, validate, validates_schema, ValidationError
from models import User
from extensions import ma  # Assuming you use Marshmallow's instance


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True  # Loads existing data if necessary
        exclude = (
            "user_id",
            "password",
        )  # ID and password should be excluded during readout

    first_name = fields.String(
        required=True,
        validate=validate.Length(min=3),
        error_messages={
            "required": "The first name is required",
            "invalid": "The first name is invalid and needs to be a string",
        },
    )
    last_name = fields.String(
        required=True,
        validate=validate.Length(min=3),
        error_messages={
            "required": "The last name is required",
            "invalid": "The last name is invalid and needs to be a string",
        },
    )
    email = fields.Email(
        required=True,
        error_messages={
            "required": "The email is required",
            "invalid": "The email format is incorrect",
        },
    )

    # Email validation to prevent duplicate entries
    @validates_schema
    def validate_email(self, data, **kwargs):
        email = data.get("email")
        if User.query.filter_by(email=email).count():
            raise ValidationError(f"Email {email} already exists.")


class UserCreateSchema(UserSchema):
    # Password field with strong validation (at least 8 characters, special characters, etc.)
    password = fields.String(
        required=True,
        validate=[
            validate.Regexp(
                r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$",
                error="The password must be at least 8 characters long and include an uppercase letter, a lowercase letter, a number, and a special character.",
            )
        ],
        error_messages={
            "required": "A password is required",
        },
    )
