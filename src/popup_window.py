import dash_html_components as html
import dash_leaflet as dl
from dash import Dash, State, callback
from dash.dependencies import Output, Input
from dash_extensions.javascript import Namespace, assign

import dash_bootstrap_components as dbc

pop_up_window_content = html.Div([
    html.H2("Country Information"),
    html.Div(id="country-info"),
    dbc.Button("Close", id="close-button")
])

popup_window = dbc.Modal(
    children=pop_up_window_content,
    id="popup-window",
    is_open=False,
)

@callback(
    Output("popup-window", "is_open"),
    Input("close-button", "n_clicks"),
    State("popup-window", "is_open"),
)
def toggle_popup(n_clicks, is_open):
    if n_clicks:
        return not is_open
    return is_open