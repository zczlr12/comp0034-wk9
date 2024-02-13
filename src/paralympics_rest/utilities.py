import datetime
from functools import wraps
from pathlib import Path

import jwt
import pandas as pd
from flask import request, make_response, current_app as app

from paralympics_rest import db
from paralympics_rest.models import User, Region, Event


def token_required(f):
    """Require valid jwt for a route

    Decorator to protect routes using jwt
    """

    @wraps(f)
    def decorator(*args, **kwargs):
        token = None
        # See if there is an Authorization section in the HTTP request headers
        if "Authorization" in request.headers:
            token = request.headers.get("Authorization")

        # If not, then return a 401 error (missing or invalid authentication credentials)
        if not token:
            response = {"message": "Authentication Token missing"}
            return make_response(response, 401)
        # Check the token is valid
        token_payload = decode_auth_token(token)
        user_id = token_payload["sub"]
        # Find the user in the database using their email address which is in the data of the decoded token
        current_user = db.session.execute(db.select(User).filter_by(id=user_id)).scalar_one_or_none()
        if not current_user:
            response = {"message": "Invalid or missing token."}
            return make_response(response, 401)
        return f(*args, **kwargs)

    return decorator


def encode_auth_token(user_id):
    """Generates the Auth Token

    :param: string user_id  The user id of the user logging in
    :return: string
    """
    try:
        # See https://pyjwt.readthedocs.io/en/latest/api.html for the parameters
        token = jwt.encode(
            # Sets the token to expire in 5 mins
            payload={
                "exp": datetime.datetime.now(datetime.UTC) + datetime.timedelta(minutes=5),
                "iat": datetime.datetime.now(datetime.UTC),
                "sub": user_id,
            },
            # Flask app secret key, matches the key used in the decode() in the decorator
            key=app.config['SECRET_KEY'],
            # Matches the algorithm in the decode() in the decorator
            algorithm='HS256'
        )
        return token
    except Exception as e:
        return e


def decode_auth_token(auth_token):
    """
    Decodes the auth token.
    :param auth_token:
    :return: token payload
    """
    # Use PyJWT.decode(token, key, algorithms) to decode the token with the public key for the app
    # See https://pyjwt.readthedocs.io/en/latest/api.html
    try:
        payload = jwt.decode(auth_token, app.config.get("SECRET_KEY"), algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        return make_response({'message': "Token expired. Please log in again."}, 401)
    except jwt.InvalidTokenError:
        return make_response({'message': "Invalid token. Please log in again."}, 401)


def add_data(db):
    """Adds data to the database if it does not already exist.

    :param db: SQLAlchemy database for the app
    """
    # Create a connection to the REST API sqlite database usinf FlaskSQLAlchemy
    connection = db.engine.connect()

    # If there are no regions in the database, then add them
    first_region = db.session.execute(db.select(Region)).first()
    if not first_region:
        print("Start adding region data to the database")
        region_file = Path(__file__).parent.parent.parent.joinpath("data", "noc_regions.csv")
        # Read the noc_regions data to a pandas dataframe
        na_values = [""]
        regions_df = pd.read_csv(region_file, keep_default_na=False, na_values=na_values)
        # Write the values to the database table
        regions_df.to_sql("region", connection, if_exists="append", index=False)

    # If there are no Events, then add them
    first_event = db.session.execute(db.select(Event)).first()
    if not first_event:
        # Read the paralympics event data to a pandas dataframe
        event_file = Path(__file__).parent.parent.parent.joinpath("data", "paralympic_events.csv")
        events_df = pd.read_csv(event_file)

        # Write the pandas DataFrame contents to the database tables
        # For the event table we want the pandas index, but it needs to start from 1 and not 0
        events_df.index += 1
        events_df.to_sql("event", connection, if_exists="append", index_label='id')

    # Close the database connection
    connection.close()
