# Standard Library imports

# Core Flask imports

# Third-party imports
import bcrypt

# App imports
from app import db_manager as db
from ..models import User, Account
from ..utils import custom_errors
from ..utils.validators import AccountValidator, EmailValidator


def get_user_profile_from_user_model(user_model):
    user_model_dict = user_model.__dict__

    allowlisted_keys = ["username", "email"]

    for key in list(user_model_dict.keys()):
        if key not in allowlisted_keys:
            user_model_dict.pop(key)

    return user_model_dict


def update_email(current_user_model, sanitized_email):
    EmailValidator(email=sanitized_email)

    if (
        db.session.query(User.email).filter_by(email=sanitized_email).first()
        is not None
    ):
        raise custom_errors.EmailAddressAlreadyExistsError()

    current_user_model.email = sanitized_email
    db.session.add(current_user_model)

    return


def create_account(sanitized_username, sanitized_email, unhashed_password):
    AccountValidator(
        username=sanitized_username,
        email=sanitized_email,
        password=unhashed_password
    )

    if (
        db.session.query(User.email).filter_by(email=sanitized_email).first()
        is not None
    ):
        raise custom_errors.EmailAddressAlreadyExistsError()

    hash = bcrypt.hashpw(unhashed_password.encode(), bcrypt.gensalt())
    password_hash = hash.decode()

    account_model = Account()
    db.session.add(account_model)
    db.session.flush()

    user_model = User(
        username=sanitized_username,
        password_hash=password_hash,
        email=sanitized_email,
        account_id=account_model.account_id,
    )

    db.session.add(user_model)
    db.session.commit()

    return user_model


def verify_login(sanitized_email, password):
    EmailValidator(email=sanitized_email)

    user_model = db.session.query(User).filter_by(email=sanitized_email).first()

    if not user_model:
        raise custom_errors.CouldNotVerifyLogin()

    if not bcrypt.checkpw(password.encode(), user_model.password_hash.encode()):
        raise custom_errors.CouldNotVerifyLogin()

    return user_model
