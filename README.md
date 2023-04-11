# flask_for_startups
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)


This flask boilerplate was written to help make it easy to iterate on your startup/indiehacker business, thereby increasing your chances of success.

Interested in learning how this works?

[![](https://www.flaskforstartups.com/imgs/get-the-book.png)](https://nuvic.gumroad.com/l/flaskforstartups)

Want to show your support? [Get me a coffee ☕](https://www.buymeacoffee.com/nuvic)

## Acknowledgements

- Alex Krupp's [django_for_startups repo](https://github.com/Alex3917/django_for_startups) and [article](https://alexkrupp.typepad.com/sensemaking/2021/06/django-for-startup-founders-a-better-software-architecture-for-saas-startups-and-consumer-apps.html)
- Miguel Grinberg's [flask mega tutorial repo](https://github.com/miguelgrinberg/microblog).

## Why is this useful?

When you're working on a project you're serious about, you want a set of conventions in place to let you develop fast and test different features. The main characteristics of this structure are:
* **Predictability**
* **Readability**
* **Simplicity**
* **Upgradability**

For side projects especially, having this structure would be useful because it would let you easily pick up the project after some time.

## Features

- Works with Python 3.9+
- [12-Factor](https://12factor.net/) based settings via [`.flaskenv` configuration handling](https://flask.palletsprojects.com/en/2.1.x/config/)
- Login and registration via [flask-login](https://github.com/maxcountryman/flask-login)
- [SQLAlchemy](https://github.com/sqlalchemy/sqlalchemy) Python SQL toolkit and ORM
- DB Migration using [Alembic](https://github.com/sqlalchemy/alembic)
- Role-based access control (RBAC) with User, UserRole, and Role models ready to go
- [Pytest](https://github.com/pytest-dev/pytest/) setup with fixtures for app and models, and integration tests with high coverage
- Validation using [pydantic](https://github.com/pydantic/pydantic)

### How is this different from other Flask tutorials?

If you haven't read the above article, what's written here is a summary of the main points, and along with how it contrasts with the Flask structure from other popular tutorials.

To make it simple to see, let's go through the `/register` route to see how a user would create an account.
* user goes to `/register`
  * flask handles this request at `routes.py`:
    * `app.add_url_rule('/register', view_func=static_views.register)`
  * you can see that the route isn't using the usual decorator `@app.route` but instead, the route is connected with a `view_func` (aka controller)
  * `routes.py` actually only lists these `add_url_rule` functions connecting a url with a view_func
  * this makes it very easy for a developer to see exactly what route matches to which view function since it's all in one file. if the urls were split up, you would have to grep through your codebase to find the relevant url
  * the view function in file `static_views.py`, `register()` simply returns the template
* user enters information on the register form (`register.html`), and submits their info
* their user details are passed along to route `/api/register`: 
  * `app.add_url_rule('/api/register', view_func=account_management_views.register_account, methods=['POST'])`
  * here the view function in file `account_management_views.py` looks like this:
  ```python
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
  ```
  * it shows linearly what functions are called for this endpoint  (*readability* and *predictability*)
  * the user input is always sanitized first, with clear variable names of what's unsafe and what's sanitized
  * then the actual account creation occurs in a `service`, which is where your business logic happens
  * if the `account_management_services.create_account` function returns an exception, it's caught here, and an appropriate error response is returned back to the user
  * otherwise, the user is logged in
* so how does the account creation service work?
  ```python
  def create_account(sanitized_username, sanitized_email):
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
  ```
  * first, the user's info has to be validated through `AccountValidator` which checks for things like, does the email exist?
  * then it checks whether the email exists in the database, and if so, raise a custom error `EmailAddressAlreadyExists`
  * otherwise, it will add the user to the database and return the `user_model`
  * notice how the variable is called `user_model` instead of just `user`, making it clear that it's an ORM representation of the user
* how do these custom errors work?
  * so if a user enters a email that already exists, it will raise this custom error from `custom_errors.py`
  ```python
  class EmailAddressAlreadyExistsError(Error):
      message = "There is already an account associated with this email address."
      internal_error_code = 40902
  ```
  * the message is externally displayed to the user, while the `internal_error_code` is more for the frontend to use in debugging. it makes it easy for the frontend to see exactly what error happened and debug it (*readability*)
  ```python
  def get_business_requirement_error_response(business_logic_error, http_status_code):
      resp = {
          "errors": {
              "display_error": business_logic_error.message,
              "internal_error_code": business_logic_error.internal_error_code,
          }
      }
      return resp, http_status_code
  ```
  * error messages are passed back to the frontend via a similar format as above: `display_error` and `internal_error_code`. the validation error message will be different in that it has field errors. (*simplicity*)
* Testing
  * the tests are mostly integration tests using a test database
  * more work could be done here, but each endpoint should be tested for: permissions, validation errors, business requirement errors, and success conditions

## Setup Instructions

Change `.sample_flaskenv` to `.flaskenv`

### Database setup

Databases supported:
- PostgreSQL
- MySQL
- SQLite

However, I've only tested using PostgreSQL.

Replace the `DEV_DATABASE_URI` with your database uri. If you're wishing to run the tests, update `TEST_DATABASE_URI`.

### Repo setup

* `git clone git@github.com:nuvic/flask_for_startups.git`
* `sudo apt-get install python3-dev` (needed to compile psycopg2, the python driver for PostgreSQL)
* If using `poetry` for dependency management
  * `poetry install
* Else use `pip` to install dependencies
  * `python3 -m venv venv`
  * activate virtual environment: `source venv/bin/activate`
  * install requirements: `pip install -r requirements.txt`
* rename `.sample_flaskenv` to `.flaskenv` and update the relevant environment variables in `.flaskenv`
* initialize the dev database: `alembic -c migrations/alembic.ini -x db=dev upgrade head`
* run server:
  * with poetry: `poetry run flask run`
  * without poetry: `flask run`

### Updating db schema

* if you make changes to models.py and want alembic to auto generate the db migration: `./scripts/db_revision_autogen.sh "your_change_here"
* if you want to write your own changes: `./scripts/db_revision_manual.sh "your_change_here"` and find the new migration file in `migrations/versions`

### Run tests

* if your test db needs to be migrated to latest schema: `alembic -c migrations/alembic.ini -x db=test upgrade head`
* `python -m pytest tests`

### Dependency management

Using [poetry](https://python-poetry.org/).

Activate poetry shell and virtual environment:
- `poetry shell`

Check for outdated dependencies:
- `poetry show --outdated`


## Other details

* Sequential IDs vs UUIDs?
  * see [brandur's article](https://brandur.org/nanoglyphs/026-ids) for a good analysis of UUID vs sequence IDs
  * instead of UUID4, you can use a sequential UUID like a [tuid](https://github.com/tanglebones/pg_tuid)
