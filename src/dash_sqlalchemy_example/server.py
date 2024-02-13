from pathlib import Path

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase

from dash_sqlalchemy_example.add_data import add_data


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)

server = Flask(__name__)

paralympic_db = Path(__file__).parent.joinpath("paralympics_dash.sqlite")
server.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + str(paralympic_db)
# server.config["SQLALCHEMY_ECHO"] = True


db.init_app(server)

# Avoid circular import
from dash_sqlalchemy_example.models import Event, Region

with server.app_context():
    db.create_all()
    connection = db.engine.connect()
    add_data(db, connection)
