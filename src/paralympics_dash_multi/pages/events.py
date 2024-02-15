# Page with the map and stats card
from dash import register_page
import dash_bootstrap_components as dbc
from paralympics_dash_multi import layout_events

import src.paralympics_dash.layout_elements

# register the page in the app
register_page(__name__, name='Events', title='Events', path="/", )

# The rows are in a separate Python module called layout_events.py
layout = dbc.Container([
    src.paralympics_dash.layout_elements.row_one,
    src.paralympics_dash.layout_elements.row_two,
])
