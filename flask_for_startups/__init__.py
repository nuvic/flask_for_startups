# Standard Library imports
import logging
from logging.handlers import RotatingFileHandler
import os

# Core Flask imports
from flask import Flask
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect

# Third-party imports

# App imports
from flask_for_startups.database import DatabaseManager
from flask_for_startups.routes import init_routes
from config import config_manager


# Load extensions
login_manager = LoginManager()
login_manager.login_view = "login"
csrf = CSRFProtect()
db_manager = DatabaseManager()


def load_logs(app):
    if app.config['LOG_TO_STDOUT']:
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(logging.INFO)
        app.logger.addHandler(stream_handler)
    else:
        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler = RotatingFileHandler('logs/flask_for_startups.log',
                                            maxBytes=10240, backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s '
            '[in %(pathname)s:%(lineno)d]'))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)

    app.logger.setLevel(logging.INFO)
    app.logger.info('flask_for_startups startup')
    return


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config_manager[config_name])

    config_manager[config_name].init_app(app)

    login_manager.login_view = "login"
    login_manager.init_app(app)

    csrf.init_app(app)

    db_manager.init_app(app)

    if not app.debug and not app.testing:
        load_logs(app)

    init_routes(app=app, db=db_manager.session)

    from flask_for_startups import models

    return app
