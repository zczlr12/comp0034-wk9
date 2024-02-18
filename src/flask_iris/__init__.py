from pathlib import Path

from flask import Flask
import logging

from flask_iris.config import app_config


from flask_iris.create_ml_model import create_model


def create_app(config_name='development'):
    """Create and configure the Flask app

    Args:
    config_name: name of the configuration environment (see config.py, app_config)

    Returns:
    Configured Flask app

    """
    log_path = Path(__file__).parent.parent.parent.joinpath('iris_app.log')
    logging.basicConfig(filename=str(log_path), level=logging.DEBUG)

    app = Flask(__name__)

    app.config.from_object(app_config[config_name])

    with app.app_context():
        from flask_iris import routes

    # If the ml model file isn't present, create it
    # Commented out, you will need to install scikit-learn if you want to run this
    create_model("lr")

    return app
