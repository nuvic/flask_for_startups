# Standard Library imports

# Core Flask imports
from flask import request, redirect, url_for

# Third-party imports
from pydantic import ValidationError
from flask_login import login_user, logout_user, login_required, current_user

# App imports
from ..services import account_management_services
from ..utils import custom_errors, sanitization
from ..utils.error_utils import (
    get_business_requirement_error_response,
    get_validation_error_response,
    get_db_error_response,
)


def register_account():
    unsafe_username = request.json.get("username")
    unsafe_email = request.json.get("email")
    unhashed_password = request.json.get("password")

    sanitized_username = sanitization.strip_xss(unsafe_username)
    sanitized_email = sanitization.strip_xss(unsafe_email)

    try:
        user_model = account_management_services.create_account(
            sanitized_username, sanitized_email, unhashed_password
        )
    except ValidationError as e:
        return get_validation_error_response(validation_error=e, http_status_code=422)
    except custom_errors.EmailAddressAlreadyExistsError as e:
        return get_business_requirement_error_response(
            business_logic_error=e, http_status_code=409
        )
    except custom_errors.InternalDbError as e:
        return get_db_error_response(db_error=e, http_status_code=500)

    login_user(user_model, remember=True)

    return {"message": "success"}, 201


def login_account():
    unsafe_email = request.json.get("email")
    password = request.json.get("password")

    sanitized_email = sanitization.strip_xss(unsafe_email)

    try:
        user_model = account_management_services.verify_login(sanitized_email, password)
    except ValidationError as e:
        return get_validation_error_response(validation_error=e, http_status_code=422)
    except custom_errors.CouldNotVerifyLogin as e:
        return get_business_requirement_error_response(
            business_logic_error=e, http_status_code=401
        )

    login_user(user_model, remember=True)

    return {"message": "success"}


def logout_account():
    logout_user()
    return redirect(url_for("index"))


@login_required
def user():
    user_profile_dict = account_management_services.get_user_profile_from_user_model(
        current_user
    )
    return {"data": user_profile_dict}


@login_required
def email():
    unsafe_email = request.json.get("email")

    sanitized_email = sanitization.strip_xss(unsafe_email)

    try:
        account_management_services.update_email(current_user, sanitized_email)
    except ValidationError as e:
        return get_validation_error_response(validation_error=e, http_status_code=422)
    except custom_errors.EmailAddressAlreadyExistsError as e:
        return get_business_requirement_error_response(
            business_logic_error=e, http_status_code=409
        )
    except custom_errors.InternalDbError as e:
        return get_db_error_response(db_error=e, http_status_code=500)

    return {"message": "success"}, 201
