# Standard Library imports

# Core Flask imports

# Third-party imports
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker, declarative_base

# App imports


class DatabaseManager:
    def __init__(self, app=None):
        self.app = app
        self.session = None
        self.engine = None
        self.base = declarative_base()

    def init_app(self, app):
        self.create_engine(app.config["SQLALCHEMY_DATABASE_URI"])
        self.create_scoped_session()
        self.base.query = self.session.query_property()

    def create_engine(self, sqlalchemy_database_uri):
        self.engine = create_engine(sqlalchemy_database_uri)

    def create_scoped_session(self):
        self.session = scoped_session(
            sessionmaker(autocommit=False, bind=self.engine)
        )
