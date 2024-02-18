import dash_bootstrap_components as dbc
from dash import html, dcc

from paralympics_dash.figures import line_chart, bar_gender, scatter_geo

# Figures
map = scatter_geo()
line = line_chart("sports")
bar = bar_gender("winter")

# Layout variables
dropdown = dbc.Select(
    id="type-dropdown",
    options=[
        {"label": "Events", "value": "events"},
        {"label": "Sports", "value": "sports"},
        {"label": "Countries", "value": "countries"},
        {"label": "Athletes", "value": "participants"},
    ],
    value="events"
)

checklist = dbc.Checklist(
    options=[
        {"label": "Summer", "value": "summer"},
        {"label": "Winter", "value": "winter"},
    ],
    value=["summer"],
    id="checklist-input",
    inline=True,
)

row_one = html.Div(
    dbc.Row([
        dbc.Col([html.H1("Paralympics Dashboard", id='heading-one'), html.P(
            "Use the charts to help you answer the questions.")
                 ], width=12),
    ]),
)

row_two = dbc.Row([
    dbc.Col(children=[
        dropdown
    ], width=2),
    dbc.Col(children=[
        checklist,
    ], width={"size": 2, "offset": 4}),
], align="start")

row_three = dbc.Row([
    dbc.Col(children=[
        dcc.Graph(id="line", figure=line),
    ], width=6),
    dbc.Col(children=[
        dcc.Graph(id="bar", figure=bar),
    ], width=6),
], align="start")

row_four = dbc.Row([
    dbc.Col(children=[
        dcc.Graph(id="map", figure=map)
    ], width=8, align="start"),
    dbc.Col(children=[
        html.Br(),
        html.Div(id='card'),
    ], width=4, align="start"),
])
