import os

class Config:
    # Generate a random secret key
    SECRET_KEY = os.urandom(24)

    # Use SQLite as the database for development
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Configuration for the user database
    USER_DATABASE = 'users.db'

