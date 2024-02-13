import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase

from paralympics_flask.utilities import add_data


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='create-your-own-key',
        SQLALCHEMY_DATABASE_URI="sqlite:///" + os.path.join(app.instance_path, 'paralympics_flask.sqlite'),
        SQLALCHEMY_ECHO=True
    )
    if test_config:
        app.config.from_mapping(test_config)
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    db.init_app(app)

    from paralympics_flask.models import User, Event, Region
    with app.app_context():
        db.create_all()
        add_data(db)

        from paralympics_flask import views

    return app
