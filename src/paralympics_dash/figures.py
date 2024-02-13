import sqlite3
from pathlib import Path

import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc
from dash import html

event_data = Path(__file__).parent.parent.parent.joinpath("data", "paralympic_events.csv")
paralympic_db = Path(__file__).parent.joinpath("paralympics.sqlite")


def line_chart(feature):
    """ Creates a line chart with data from paralympics_events.csv

    Data is displayed over time from 1960 onwards.
    The figure shows separate trends for the winter and summer events.

     Parameters
     feature: events, sports or participants

     Returns
     fig: Plotly Express line figure
     """

    # take the feature parameter from the function and check it is valid
    if feature not in ["sports", "participants", "events", "countries"]:
        raise ValueError(
            'Invalid value for "feature". Must be one of ["sports", "participants", "events", "countries"]')
    else:
        # Make sure it is lowercase to match the dataframe column names
        feature = feature.lower()

    # Read the data from pandas into a dataframe
    cols = ["type", "year", "host", "events", "sports", "participants", "countries"]
    line_chart_data = pd.read_csv(event_data, usecols=cols)

    # Set the title for the chart using the value of 'feature'
    title_text = f"How has the number of {feature} changed over time?"

    '''
    Create a Plotly Express line chart with the following parameters
      line_chart_data is the DataFrane
      x="year" is the column to use as a x-axis
      y=feature is the column to use as the y-axis
      color="type" indicates if winter or summer
      title=title_text sets the title using the variable title_text
      labels={} sets the X label to Year, sets the Y axis and the legend to nothing (an empty string)
      template="simple_white" uses a Plotly theme to style the chart
    '''
    fig = px.line(line_chart_data,
                  x="year",
                  y=feature,
                  color="type",
                  title=title_text,
                  labels={'year': 'Year', feature: '', 'type': ''},
                  template="simple_white"
                  )
    return fig


def bar_gender(event_type):
    """
    Creates a stacked bar chart showing change in the number of sports in the summer and winter paralympics
    over time
    An example for exercise 2.

    :param event_type: str Winter or Summer
    :return: Plotly Express bar chart
    """
    cols = ['type', 'year', 'host', 'participants_m', 'participants_f', 'participants']
    df_events = pd.read_csv(event_data, usecols=cols)
    # Drop Rome as there is no male/female data
    df_events.drop([0], inplace=True, )
    df_events.reset_index(drop=True)
    # Add new columns that each contain the result of calculating the % of male and female participants
    df_events['M%'] = df_events['participants_m'] / df_events['participants']
    df_events['F%'] = df_events['participants_f'] / df_events['participants']
    # Sort the values by Type and Year
    df_events.sort_values(['type', 'year'], ascending=(True, True), inplace=True)
    # Create a new column that combines Location and Year to use as the x-axis
    df_events['xlabel'] = df_events['host'] + ' ' + df_events['year'].astype(str)
    # Create the stacked bar plot of the % for male and female
    df_events = df_events.loc[df_events['type'] == event_type]
    fig = px.bar(df_events,
                 x='xlabel',
                 y=['M%', 'F%'],
                 title='How has the ratio of female:male participants changed?',
                 labels={'xlabel': '', 'value': '', 'variable': ''},
                 color_discrete_map={'M%': 'blue', 'F%': 'green'},
                 template="simple_white"
                 )
    fig.update_xaxes(ticklen=0)
    return fig


def scatter_mapbox():
    """
    Create a Scatter mapbox showing the locations of the paralympic events.

    This version requires you to create a mapbox token
    see https://plotly.com/python/scattermapbox/

    """
    # create database connection
    connection = sqlite3.connect(paralympic_db)

    # define the sql query
    sql = '''
    SELECT event.id, event.host, event.year, location.lat, location.lon
    FROM event
    JOIN location ON event.host = location.city 
    '''

    df_locs = pd.read_sql(sql=sql, con=connection, index_col=None)
    df_locs['lon'] = df_locs['lon'].astype(float)
    df_locs['lat'] = df_locs['lat'].astype(float)

    px.set_mapbox_access_token(open(".mapbox_token").read())

    fig = px.scatter_mapbox(df_locs,
                            lat='lat',
                            lon='lon',
                            zoom=1,
                            hover_data=['host', 'year'],
                            mapbox_style='carto-positron',
                            center=dict(lat=df_locs['lat'][0],
                                        lon=df_locs['lon'][0])
                            )

    return fig


def scatter_geo():
    # create database connection
    connection = sqlite3.connect(paralympic_db)

    # define the sql query
    sql = '''
        SELECT event.id, event.host, event.year, location.lat, location.lon
        FROM event
        JOIN location ON event.host = location.city 
        '''

    df_locs = pd.read_sql(sql=sql, con=connection, index_col=None)
    df_locs['lon'] = df_locs['lon'].astype(float)
    df_locs['lat'] = df_locs['lat'].astype(float)
    df_locs['name'] = df_locs['host'] + ' ' + df_locs['year'].astype(str)

    fig = px.scatter_geo(df_locs,
                         lat=df_locs.lat,
                         lon=df_locs.lon,
                         hover_name=df_locs.name,
                         title="Where have the paralympics been held?"
                         )
    return fig
