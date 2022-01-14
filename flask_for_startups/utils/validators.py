# Standard Library imports

# Core Flask imports

# Third-party imports
from marshmallow import Schema, fields, validate

# App imports


class AccountValidator(Schema):
    username = fields.Str(
        required=True,
        load_only=True,
        validate=[
            validate.Length(
                1, 15, error="Usernames must be less than or equal to 15 characters."
            ),
            validate.Regexp(
                "^[a-zA-Z][a-zA-Z0-9_]*$",
                error="Username must start with a letter, and "
                "contain only letters, numbers, and underscores.",
            ),
        ],
    )
    email = fields.Email(required=True, load_only=True)


class EmailValidator(Schema):
    email = fields.Email(required=True, load_only=True)
