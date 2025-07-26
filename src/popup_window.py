import dash_html_components as html
import dash_leaflet as dl
from dash import Dash, State, callback
from dash.dependencies import Output, Input
from dash_extensions.javascript import Namespace, assign

import dash_bootstrap_components as dbc

pop_up_window = html.Div([
    html.H2("Country Information"),
    html.Div(id="country-info"),
    dbc.Button("Close", id="close-button")
])