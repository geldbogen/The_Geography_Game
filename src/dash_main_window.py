import dash_html_components as html
import dash_leaflet as dl
from dash import Dash, State, callback
from dash.dependencies import Output, Input
from dash_extensions.javascript import Namespace, assign




def create_main_window_layout():

    ns = Namespace("myNamespace", "mySubNamespace")
    style_handle = ns('my_style')

    return html.Div([
        html.H1("Geography Game"),
        dl.Map(center=[39, -98], zoom=4, children=[
            dl.TileLayer(),
            dl.GeoJSON(url='/assets/world_map.geojson', id="main-window-geojson",
                    options=dict(style=style_handle), 
                    hideout=dict(selected=[]),
                    ),
        ], style={'width': '100%', 'height': '100vh'}, id="map"),
        html.Div(id="info")
    ])


@callback(
    Output("main-window-geojson", "hideout"),
    Input("main-window-geojson", "n_clicks"),
    State("main-window-geojson", "clickData"),
    State("main-window-geojson", "hideout"),
    prevent_initial_call=True,
)
def toggle_select(_, feature, hideout):
    selected = hideout["selected"]

    print(feature['properties']['name'])
    name = feature["properties"]["name"]
    if name in selected:
        selected.remove(name)
    else:
        selected.append(name)
    return hideout

