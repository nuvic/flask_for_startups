# Standard Library imports

# Core Flask imports

# Third-party imports

# App imports
from flask_for_startups.models import User


def test_index(client):
    response = client.get("/")
    assert response.status_code == 200


def test_register_view(client):
    response = client.get("/register")

    # test that viewing page renders without template errors
    assert response.status_code == 200


def test_register_service(client, db, user_details):
    response = client.post(
        "/api/register",
        json={"username": user_details.test_username, "email": user_details.test_email},
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
        json={"username": user_details.test_username, "email": user_details.test_email},
    )

    assert response.status_code == 201

    # test that duplicate email registrations are not allowed
    response_duplicate = client.post(
        "/api/register",
        json={"username": user_details.test_username, "email": user_details.test_email},
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

    email_error_response = response.json["errors"]["field_errors"]["email"][0]
    assert response.status_code == 422
    assert email_error_response == "Field may not be null."


def test_login_success(client, db, existing_user):
    login_view_response = client.get("/login")

    assert login_view_response.status_code == 200

    response = client.post(
        "/api/login",
        json={"username": existing_user.username, "email": existing_user.email},
    )

    assert response.status_code == 200
    assert response.json["message"] == "success"


def test_login_fail(client, db):
    response = client.post(
        "/api/login", json={"username": "fake", "email": "fake@email.com"}
    )

    response_display_error = response.json["errors"]["display_error"]
    expected_display_error = (
        "There is no user with the entered credentials. Please try again."
    )

    assert response.status_code == 401
    assert response_display_error == expected_display_error


def test_logout(client, db, existing_user):
    client.post(
        "/api/login",
        json={"username": existing_user.username, "email": existing_user.email},
    )

    response = client.get("/api/logout")
