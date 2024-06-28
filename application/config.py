import os
from datetime import timedelta

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    DEBUG = False
    SQLITE_DB_DIR = None
    SQLALCHEMY_DATABASE_URI = None
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=3)
    TIMEZONE = 'Asia/Kolkata'
    MAIL_SERVER = "smtp.mailtrap.io"
    MAIL_PORT = 2525
    MAIL_USERNAME = "<your_mailtrap_username>"
    MAIL_PASSWORD = "<your_mailtrap_password>"
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    CELERY_BROKER_URL = "redis://localhost:6379/1"
    CELERY_RESULT_BACKEND = "redis://localhost:6379/2"


class LocalDevelopmentConfig(Config):
    DEBUG = True
    SQLITE_DB_DIR = os.path.join(basedir, '../db_dir')
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(SQLITE_DB_DIR, 'mydb.sqlite3')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CELERY_BROKER_URL = "redis://localhost:6379/1"
    CELERY_RESULT_BACKEND = "redis://localhost:6379/2"


class ProductionDevelopmentConfig(Config):
    DEBUG = False
    SQLITE_DB_DIR = os.path.join(basedir, '../db_dir')
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(SQLITE_DB_DIR, 'mydb.sqlite3')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
