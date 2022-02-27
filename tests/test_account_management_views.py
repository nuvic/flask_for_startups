# Standard Library imports

# Core Flask imports

# Third-party imports

# App imports
from app.models import User
from app.utils.custom_errors import CouldNotVerifyLogin


def test_index(client):
    response = client.get("/")
    assert response.status_code == 200


def test_register_view(client):
    response = client.get("/register")

    assert response.status_code == 200


def test_register_service(client, db, user_details):
    response = client.post(
        "/api/register",
        json={
            "username": user_details.test_username,
            "email": user_details.test_email,
            "password": user_details.test_password,
        },
    )

    # test successful account registration
    assert response.status_code == 201

    # test that user was inserted into database
    user_model = db.session.query(User).filter_by(email=user_details.test_email).first()
    assert user_model is not None
    assert user_model.username == user_details.test_username
    assert user_model.email == user_details.test_email


def test_register_service_reject_duplicates(client, db, user_details):
    response = client.post(
        "/api/register",
        json={
            "username": user_details.test_username,
            "email": user_details.test_email,
            "password": user_details.test_password,
        },
    )

    assert response.status_code == 201

    # test that duplicate email registrations are not allowed
    response_duplicate = client.post(
        "/api/register",
        json={
            "username": user_details.test_username,
            "email": user_details.test_email,
            "password": user_details.test_password,
        },
    )

    assert response_duplicate.status_code == 409

    user_model_list = (
        db.session.query(User).filter_by(email=user_details.test_email).all()
    )

    # test that only one user exists with the registered email
    assert len(user_model_list) == 1


def test_register_service_requires_email(client, db, user_details):
    response = client.post(
        "/api/register", json={"username": user_details.test_username}
    )

    assert response.status_code == 422

    email_error_response = response.json["errors"]["field_errors"]["email"][0]
    assert email_error_response == "Field may not be null."

    password_error_response = response.json["errors"]["field_errors"]["password"][0]
    assert password_error_response == "Field may not be null."


def test_login_success(client, existing_user, user_details):
    login_view_response = client.get("/login")

    assert login_view_response.status_code == 200

    response = client.post(
        "/api/login",
        json={"email": existing_user.email, "password": user_details.test_password},
    )

    assert response.status_code == 200
    assert response.json["message"] == "success"


def test_login_fail(client, existing_user):
    response = client.post(
        "/api/login",
        json={"email": existing_user.email, "password": "fake password"},
    )

    response_display_error = response.json["errors"]["display_error"]

    assert response.status_code == 401
    assert response_display_error == CouldNotVerifyLogin.message


def test_logout(client, existing_user, user_details):
    client.post(
        "/api/login",
        json={"email": existing_user.email, "password": user_details.test_password},
    )

    response = client.get("/logout", follow_redirects=True)

    # check that the path changed
    assert response.request.path == "/"
