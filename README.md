# flask_for_startups
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

The purpose of this project:

> I wrote this guide to explain how to write software in a way that maximizes the number of chances your startup has to succeed — by making it easy to maintain development velocity regardless of the inevitable-but-unknowable future changes to team size, developer competence and experience, product functionality, etc. The idea is that, given the inherent uncertainty, startups can massively increase their odds of success by putting some basic systems in place to help maximize the number of ideas, features, and hypotheses they can test; in other words, maximizing "lead bullets," to borrow the phrase from this [blog post](https://a16z.com/2011/11/13/lead-bullets/) by Ben Horowitz.
> From Alex Kurpp's article Alex Krupp's article [Django for Startup Founders: A better software architecture for SaaS startups and consumer apps](https://alexkrupp.typepad.com/sensemaking/2021/06/django-for-startup-founders-a-better-software-architecture-for-saas-startups-and-consumer-apps.html)

## Why is this useful?

When you're working on a project you're serious about, you want a set of conventions in place to let you develop fast and test different features. The main characteristics of this structure are:
* **Predictability**
* **Readability**
* **Simplicity**
* **Upgradability**

For side projects especially, having this structure would be useful because it would let you easily pick up the project after some time.

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
    unsafe_username = request.json.get('username')
    unsafe_email = request.json.get('email')

    sanitized_username = sanitization.strip_xss(unsafe_username)
    sanitized_email = sanitization.strip_xss(unsafe_email)

    try:
        user_model = account_management_services.create_account(sanitized_username, sanitized_email)
    except marshmallow.exceptions.ValidationError as e:
        return get_validation_error_response(validation_error=e, http_status_code=422)
    except custom_errors.EmailAddressAlreadyExistsError as e:
        return get_business_requirement_error_response(business_logic_error=e, http_status_code=409)
    except custom_errors.InternalDbError as e:
        return get_db_error_response(db_error=e, http_status_code=500)

    login_user(user_model, remember=True)

    return {'message': 'success'}, 201
  ```
  * it shows linearly what functions are called for this endpoint  (*readability* and *predictability*)
  * the user input is always sanitized first, with clear variable names of what's unsafe and what's sanitized
  * then the actual account creation occurs in a `service`, which is where your business logic happens
  * if the `account_management_services.create_account` function returns an exception, it's caught here, and an appropriate error response is returned back to the user
  * otherwise, the user is logged in
* so how does the account creation service work?
  ```python
  def create_account(sanitized_username, sanitized_email):
      fields_to_validate_dict = {
          "username": sanitized_username,
          "email": sanitized_email
      }

      AccountValidator().load(fields_to_validate_dict)

      if db.session.query(User.email).filter_by(email=sanitized_email).first() is not None:
          raise custom_errors.EmailAddressAlreadyExistsError()

      account_model = Account()
      db.session.add(account_model)
      db.session.flush()

      user_model = User(username=sanitized_username, email=sanitized_email, account_id=account_model.account_id)
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

## Instructions

### PostgreSQL setup

`sudo apt install postgresql postgresql-contrib`

Creating a new role:
```
sudo -u postgres psql
> create user your_user
> \password your_password
```

Creating a development database with necessary extensions:
```
sudo su postgres
createdb your_database_name
psql -d your_database_name
> grant all privileges on database your_database_name to your_user
> create extension if not exists pgcrypto with schema public;
> create extension if not exists "uuid-ossp" with schema public
```

(Optional: only if you want to run tests). Creating a test database with necessary extensions:
```
sudo su postgres
createdb your_test_database_name
psql -d your_test_database_name
> grant all privileges on database your_test_database_name to your_user
> create extension if not exists pgcrypto with schema public;
> create extension if not exists "uuid-ossp" with schema public
```

### Repo setup

* clone repo
* `python3 -m venv venv`
* activate virtual environment: `source venv/bin/activate`
* install requirements: `pip install -r requirements.txt`
* rename `.sample_flaskenv` to `.flaskenv` and update the relevant environment variables in `.flaskenv`
    * specifically: BASE_DIR, DEV_DATABASE_URI, DB_NAME, TEST_DATABASE_URI
* initialize the dev database: `./scripts/db_migrate_dev.sh`
* run server: `flask run`

### Updating db schema

* if you make changes to models.py and want alembic to auto generate the db migration: `./scripts/db_revision_autogen.sh "your_change_here"
* if you want to write your own changes: `./scripts/db_revision_manual.sh "your_change_here" and find the new migration file in `migrations/versions`

### Run tests

* if your test db needs to be migrated to latest schema: `./scripts/db_migrate_test.sh`
* `python -m pytest tests`

## Other details

* Why UUIDs as primary key?
  * see [brandur's article](https://brandur.org/nanoglyphs/026-ids) for a good analysis of UUID vs sequence IDs
  * instead of UUID4, you can use a sequential UUID like a [tuid](https://github.com/tanglebones/pg_tuid)


## Acknowledgements

- Alex Krupp's repo [django_for_startups](https://github.com/Alex3917/django_for_startups)
- Miguel Grinberg's [flask mega tutorial repo](https://github.com/miguelgrinberg/microblog).