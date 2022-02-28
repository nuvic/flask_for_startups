# Standard Library imports
import pytest

# Core Flask imports

# Third-party imports
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import event
from sqlalchemy import create_engine
import bcrypt

# App imports
from app import create_app, db_manager
from app.models import Base, User, Account


@pytest.fixture(scope="session")
def app(request):
    app = create_app(config_name="test")

    # Get clean test database: delete data from all tables in the test db
    for table in reversed(Base.metadata.sorted_tables):
        session = db_manager.session()
        session.execute(table.delete())
        session.commit()

    # Establish an application context before running the tests.
    ctx = app.app_context()
    ctx.push()

    def teardown():
        ctx.pop()

    request.addfinalizer(teardown)
    return app


@pytest.fixture(scope="session")
def client(app):
    """A test client for the app."""
    return app.test_client()


@pytest.fixture(scope="session")
def _connection(app):
    engine = create_engine(app.config["SQLALCHEMY_DATABASE_URI"])
    connection = engine.connect()
    yield connection
    connection.close()


# Session = scoped_session(sessionmaker())
@pytest.fixture(scope="session")
def _scoped_session(app):
    Session = scoped_session(sessionmaker())
    return Session


@pytest.fixture(autouse=True)
def db(_connection, _scoped_session, request):
    # Bind app's db session to the test session
    transaction = _connection.begin()
    Session = _scoped_session
    session = Session(bind=_connection)
    session.begin_nested()

    @event.listens_for(session, "after_transaction_end")
    def restart_savepoint(db_session, transaction):
        """Support tests with rollbacks.

        if the database supports SAVEPOINT (SQLite needs special
        config for this to work), starting a savepoint
        will allow tests to also use rollback within tests

        Reference: https://docs.sqlalchemy.org/en/14/orm/session_transaction.html#session-begin-nested  # noqa: E501
        """
        if transaction.nested and not transaction._parent.nested:
            # ensure that state is expired the way session.commit() at
            # the top level normally does
            session.expire_all()
            session.begin_nested()

    """
    Important. This step binds the app's db session to the test session
    to allow each individual test to be wrapped in a transaction
    and rollback to a clean state after each test
    """
    db_manager.session = session

    def teardown():
        Session.remove()
        transaction.rollback()

    request.addfinalizer(teardown)

    yield db_manager


@pytest.fixture()
def user_details():
    class UserDetails(object):
        test_username = "test_user"
        test_email = "test@email.com"
        test_password = "my_secure_password"

    return UserDetails


@pytest.fixture()
def existing_user(db, user_details):
    account_model = Account()
    db.session.add(account_model)
    db.session.flush()

    hash = bcrypt.hashpw(user_details.test_password.encode(), bcrypt.gensalt())
    password_hash = hash.decode()

    user_model = User(
        username=user_details.test_username,
        password_hash=password_hash,
        email=user_details.test_email,
        account_id=account_model.account_id,
    )
    db.session.add(user_model)
    db.session.commit()
    return user_model
