import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.flaskenv'))

class Config(object):
    WTF_CSRF_SECRET_KEY = os.environ.get('WTF_CSRF_SECRET_KEY')
    SECRET_KEY = os.environ.get('SECRET_KEY')
    BASE_DIR = os.environ.get('BASE_DIR')
    SESSION_COOKIE_HTTPONLY = os.environ.get('SESSION_COOKIE_HTTPONLY')
    REMEMBER_COOKIE_HTTPONLY = os.environ.get('REMEMBER_COOKIE_HTTPONLY')
    SESSION_COOKIE_SAMESITE = os.environ.get('SESSION_COOKIE_SAMESITE')

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URI')


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URI')
    WTF_CSRF_ENABLED = False


config_manager = {
    'dev': DevelopmentConfig,
    'test': TestingConfig
}