from pathlib import Path

import pandas as pd


def add_data(db, connection):
    """Adds data to the database if it does not already exist.

    :param db: SQLAlchemy database for the app
    :param connection: SQLAlchemy database connection for the app
    """
    # Avoids circular import
    from dash_sqlalchemy_example.models import Region, Event

    first_region = db.session.execute(db.select(Region)).first()
    if not first_region:
        region_file = Path(__file__).parent.parent.parent.joinpath("data", "noc_regions.csv")
        regions_df = pd.read_csv(region_file, keep_default_na=False, na_values=[""])
        regions_df.to_sql("region", con=connection, if_exists="append", index=False)

    first_event = db.session.execute(db.select(Event)).first()
    if not first_event:
        event_file = Path(__file__).parent.parent.parent.joinpath("data", "paralympic_events.csv")
        events_df = pd.read_csv(event_file)
        events_df.index += 1
        events_df.to_sql("event", con=connection, if_exists="append", index_label='id')
