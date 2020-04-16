from os import environ


class Config:
    """Set Flask configuration vars from .env file."""

    # General
    FLASK_DEBUG = True
    FLASK_ENV = "development"

    # Database
    SQLALCHEMY_DATABASE_URI = "sqlite:////database/database.sqlite3"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
