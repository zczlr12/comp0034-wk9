from flask import Flask
from flask_iris.config import Config
from flask_iris.create_ml_model import create_model


def create_app(test_config=None):
    """Create and configure the Flask app

    Args:
    config_object: configuration class (see config.py)

    Returns:
    Configured Flask app

    """
    app = Flask(__name__)

    app.config.from_object(config.DevConfig)

    if test_config:
        app.config.from_object(config.TestConfig)

    # Include the routes from routes.py
    with app.app_context():
        from flask_iris import routes

    # If the ml model file isn't present, create it
    create_model("lr")

    return app
