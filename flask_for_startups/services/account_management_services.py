# Standard Library imports

# Core Flask imports

# Third-party imports
import marshmallow

# App imports
from flask_for_startups import db_manager as db
from flask_for_startups.models import User, Account
from flask_for_startups.utils import custom_errors
from flask_for_startups.utils.validators import AccountValidator, EmailValidator


def get_user_profile_from_user_model(user_model):
    user_model_dict = user_model.__dict__

    allowlisted_keys = ["username", "email"]

    for key in list(user_model_dict.keys()):
        if not key in allowlisted_keys:
            user_model_dict.pop(key)

    return user_model_dict


def update_email(current_user_model, sanitized_email):
    EmailValidator().load({"email": sanitized_email})

    if (
        db.session.query(User.email).filter_by(email=sanitized_email).first()
        is not None
    ):
        raise custom_errors.EmailAddressAlreadyExistsError()

    current_user_model.email = sanitized_email
    db.session.add(current_user_model)

    return


def create_account(sanitized_username, sanitized_email):
    fields_to_validate_dict = {"username": sanitized_username, "email": sanitized_email}

    AccountValidator().load(fields_to_validate_dict)

    if (
        db.session.query(User.email).filter_by(email=sanitized_email).first()
        is not None
    ):
        raise custom_errors.EmailAddressAlreadyExistsError()

    account_model = Account()
    db.session.add(account_model)
    db.session.flush()

    user_model = User(
        username=sanitized_username,
        email=sanitized_email,
        account_id=account_model.account_id,
    )
    db.session.add(user_model)
    db.session.commit()

    return user_model


def verify_login(sanitized_username, sanitized_email):
    fields_to_validate_dict = {"username": sanitized_username, "email": sanitized_email}

    AccountValidator().load(fields_to_validate_dict)

    user_model = (
        db.session.query(User)
        .filter_by(email=sanitized_email, username=sanitized_username)
        .first()
    )

    if not user_model:
        raise custom_errors.UserDoesNotExistError()

    return user_model
