"""Flask configuration."""
from pathlib import Path

# Sets the project root folder
PROJECT_ROOT = Path(__file__).parent


class Config:
    """Base config."""

    SECRET_KEY = "saULPgD9XU8vzLVk7kyLBw"
    # configure the SQLite database location
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + str(
        PROJECT_ROOT.joinpath("data", "iris.db")
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False


class ProdConfig(Config):
    """Production config.

    Not currently implemented.
    """

    pass


class DevConfig(Config):
    """Development config"""

    FLASK_ENV = "development"
    DEBUG = True
    TESTING = True


class TestConfig(Config):
    """Testing config"""

    TESTING = True
    SQLALCHEMY_ECHO = True
    WTF_CSRF_ENABLED = False  # Needs to be turned off for testing
    # Does not force the server to start on this port, only references the server at this address
    # You need to configure run to the same port as server name
    # SERVER_NAME = "127.0.0.1:5000"


app_config = {
    "development": DevConfig,
    "production": ProdConfig,
    "test": TestConfig
}
