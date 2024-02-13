""" Contains variables for all the rows and elements in the 'charts' page """
import dash_bootstrap_components as dbc
from dash import html, dcc, get_asset_url
from paralympics_dash_multi.figures import scatter_geo, get_event_data

# Create the scatter map
map = scatter_geo()


def create_card(event_id, method):
    """
    Generate a card for the event specified by event_id.

    Uses the REST API route or pandas DataFrame to gey the data.
    If REST API then the REST API must be running on port 5000.

    Args:
        event_id: the event it
        method: the method to access the data, either rest - REST API or df - pandas DataFrame

    Returns:
        card: dash boostrap components card for the event
    """
    ev = get_event_data(event_id, method)

    # Variables for the card contents
    logo = f'logos/{ev['year']}_{ev['host']}.jpg'
    dates = f'{ev['start']} to {ev['end']}'
    host = f'{ev['host']} {ev['year']}'
    highlights = f'Highlights: {ev['highlights']}'
    participants = f'{ev['participants']} athletes'
    events = f'{ev['events']} events'
    countries = f'{ev['countries']} countries'

    card = dbc.Card([
        dbc.CardBody(
            [
                html.H4([html.Img(src=get_asset_url(logo), width=35, className="me-1"),
                         host]),
                html.Br(),
                html.H6(dates, className="card-subtitle"),
                html.P(highlights, className="card-text"),
                html.P(participants, className="card-text"),
                html.P(events, className="card-text"),
                html.P(countries, className="card-text"),
            ]
        ),
    ],
        style={"width": "18rem"},
    )
    return card


# Create a specific instance of the card using the data for the event with id 12
# This will be replaced next week with a dynamic input using a callback

# Create the card using data from REST API, the REST app must be running on port 5000
# card = create_card(12, method="rest")

# This version uses the dataframe instead of REST API so that you don't have to run the Flask REST API app
card = create_card(12, method="pandas")

row_one = html.Div(
    dbc.Row([
        dbc.Col([html.H1("Event Details"), html.P(
            "Event details. Select a marker on the map to display the event highlights and summary data.")
                 ], width=12),
    ]),
)

row_two = html.Div(
    dbc.Row([
        dbc.Col(children=[
            # Chart replaced the placeholder image
            dcc.Graph(figure=map, id="geo-map"),
        ], width=8),
        dbc.Col(children=[
            card,
        ], width=4),
    ], align="start")
)
