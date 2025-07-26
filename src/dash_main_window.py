
import dash_leaflet as dl
from dash import Dash, State, html, callback
from dash.dependencies import Output, Input
from dash_extensions.javascript import Namespace, assign

from country import call_country_by_name
from game_state import BACKEND_GAME, get_backend_game

import popup_window


class MainWindow():

    def __init__(self):
        pass

def create_main_window_layout():

    ns = Namespace("myNamespace", "mySubNamespace")
    style_handle = ns('my_style')

    backend_game = get_backend_game()

    return html.Div([
        html.H1("Geography Game"),
        dl.Map(center=[39, -98], zoom=4, children=[
            dl.TileLayer(),
            dl.GeoJSON(url='/assets/world_map.geojson', id="main-window-geojson",
                    options=dict(style=style_handle), 
                    hideout=backend_game.hideout_dict_for_dash,
                    ),
        ], style={'width': '100%', 'height': '90vh'}, id="map"),
        html.Div(id="info"),
        popup_window.popup_window,  # Include the popup window component
    ])


@callback(
    [Output("main-window-geojson", "hideout"),
     Output("info", "children"),
     Output("popup-window", "is_open", allow_duplicate=True),
     Output("win_or_lose_title", "children")],
    Input("main-window-geojson", "n_clicks"),
    State("main-window-geojson", "clickData"),
    State("main-window-geojson", "hideout"),
    prevent_initial_call=True,
)
def click_on_map(_, feature, hideout):
    backend_game = get_backend_game()
    country = call_country_by_name(feature["properties"]["name"])
    owner = country.owner

    to_display_string = 'ERROR'
    popup_window_is_open = False
    win_or_lose = 'ERROR'

    match backend_game.chosen_country_1, backend_game.chosen_country_2:
        case None, None:
            backend_game.chosen_country_1 = country
            to_display_string = f'You have selected: {country.name} \n \
                Click on another country which you want to attack it with'
            
            # return hideout, f'You have selected: {country.name}'
        case _, None:
            backend_game.chosen_country_2 = country
            to_display_string = f'Do you want to attack {country.name} with {backend_game.chosen_country_1.name}? \n \
                Click again to confirm click somewhere else to go back to country selection'

        case a, b if a is not None and b is not None:
            if b == country:
                result = backend_game.attack_backend()
                popup_window_is_open = True
                win_or_lose = result

                to_display_string = f'It\'s {backend_game.active_player.name}\'s turn to attack'
                
            else:
                backend_game.chosen_country_1 = None
                backend_game.chosen_country_2 = None
                to_display_string = f'It\'s {backend_game.active_player.name}\'s turn to attack'

    
    hideout = backend_game.hideout_dict_for_dash
    print(f"hideout: {hideout}")
    if backend_game.chosen_country_1:
        hideout["selected"] = [backend_game.chosen_country_1.name, backend_game.chosen_country_2.name] if backend_game.chosen_country_2 else [backend_game.chosen_country_1.name]
    else:
        hideout["selected"] = []

    return hideout, html.H1(to_display_string), popup_window_is_open, win_or_lose

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