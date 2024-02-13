from pathlib import Path

import pandas as pd

from paralympics_rest.models import Region, Event


def add_data(db):
    """Adds data to the database if it does not already exist.

    :param db: SQLAlchemy database for the app
    """
    # Create a connection to the REST API sqlite database using FlaskSQLAlchemy
    connection = db.engine.connect()

    # If there are no regions in the database, then add them
    first_region = db.session.execute(db.select(Region)).first()
    if not first_region:
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
