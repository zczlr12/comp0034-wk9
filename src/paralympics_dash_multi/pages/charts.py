# Line and bar charts page
from dash import register_page
import dash_bootstrap_components as dbc
from paralympics_dash_multi import layout_charts

# register the page in the app
register_page(__name__, name="Charts", title="Charts")

# The rows are in a separate Python module called layout_charts.py
layout = dbc.Container([
    layout_charts.row_one,
    layout_charts.row_two,
])
