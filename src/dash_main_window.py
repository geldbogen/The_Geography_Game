import dash_html_components as html
import dash_leaflet as dl
from dash import Dash, State, callback
from dash.dependencies import Output, Input
from dash_extensions.javascript import Namespace, assign

from country import call_country_by_name


class MainWindow():

    def __init__(self):
        pass

def create_main_window_layout():

    ns = Namespace("myNamespace", "mySubNamespace")
    style_handle = ns('my_style')

    player_color_dict = {
        "Player 1": "blue",
        "Player 2": "red",
    }
    country_owner_dict = {
        "United States of America": "Player 1",
        "Canada": "Player 2",
        # Add more countries and their owners as needed
    }
    hideout = {
        "selected": [],
        "player_color_dict": player_color_dict,
        "country_owner_dict": country_owner_dict
    }

    return html.Div([
        html.H1("Geography Game"),
        dl.Map(center=[39, -98], zoom=4, children=[
            dl.TileLayer(),
            dl.GeoJSON(url='/assets/world_map.geojson', id="main-window-geojson",
                    options=dict(style=style_handle), 
                    hideout=hideout,
                    ),
        ], style={'width': '100%', 'height': '80vh'}, id="map"),
        html.Div(id="info")
    ])


@callback(
    [Output("main-window-geojson", "hideout"),
     Output("info", "children")],
    Input("main-window-geojson", "n_clicks"),
    State("main-window-geojson", "clickData"),
    State("main-window-geojson", "hideout"),
    prevent_initial_call=True,
)
def toggle_select(_, feature, hideout):
    selected = hideout["selected"]

    print(feature['properties']['name'])
    country_name = feature["properties"]["name"]
    print(f'Selected country: {call_country_by_name(country_name).name}')
    if country_name in selected:
        selected.remove(country_name)
    else:
        selected.append(country_name)
    global BACKEND_GAME 
    BACKEND_GAME.
    return hideout, f'You have selected: {call_country_by_name(country_name).name}'

if __name__ == "__main__":
    app = Dash(__name__)
    app.layout = create_main_window_layout()
    
    # # Register the callback
    # app.callback(
    #     [Output("main-window-geojson", "hideout"),
    #      Output("info", "children")],
    #     Input("main-window-geojson", "n_clicks"),
    #     State("main-window-geojson", "clickData"),
    #     State("main-window-geojson", "hideout"),
    #     prevent_initial_call=True,
    # )(toggle_select)
    
    app.run(debug=True)