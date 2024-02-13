import dash
import dash_bootstrap_components as dbc
from dash import Dash, html

# Variable that contains the external_stylesheet to use, in this case Bootstrap styling from dash bootstrap
# components (dbc)
external_stylesheets = [dbc.themes.BOOTSTRAP]

# Define a variable that contains the meta tags
meta_tags = [
    {"name": "viewport", "content": "width=device-width, initial-scale=1"},
]

# Pass the stylesheet variable to the Dash app constructor
app = Dash(__name__, external_stylesheets=external_stylesheets, meta_tags=meta_tags, use_pages=True)

# From https://dash-bootstrap-components.opensource.faculty.ai/docs/components/navbar/
navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Event Details", href=dash.page_registry['pages.events']['path'])),
        dbc.NavItem(dbc.NavLink("Charts", href=dash.page_registry['pages.charts']['path'])),
    ],
    brand="Paralympics Dashboard",
    brand_href="#",
    color="primary",
    dark=True,
)

app.layout = html.Div([
    # Nav bar
    navbar,
    # Area where the page content is displayed
    dash.page_container
])

if __name__ == '__main__':
    app.run(debug=True, port=8051)
