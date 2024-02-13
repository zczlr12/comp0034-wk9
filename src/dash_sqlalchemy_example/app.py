from dash import Dash, dcc, html
from dash_sqlalchemy_example.server import server

from dash_sqlalchemy_example.chart import line_chart

# Uses the Flask server created in server.py
app = Dash(__name__, server=server)

line_chart = line_chart("events")

app.layout = html.Div([
    dcc.Graph(id="line", figure=line_chart)
])

if __name__ == '__main__':
    app.run(debug=True, port=8050)