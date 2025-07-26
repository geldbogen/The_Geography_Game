import dash_html_components as html
import dash_leaflet as dl
from dash import Dash, State, callback
from dash.dependencies import Output, Input
from dash_extensions.javascript import Namespace, assign

from country import call_country_by_name
from game_state import BACKEND_GAME

import popup_window


class MainWindow():

    def __init__(self):
        pass

def create_main_window_layout():

    ns = Namespace("myNamespace", "mySubNamespace")
    style_handle = ns('my_style')


    return html.Div([
        html.H1("Geography Game"),
        dl.Map(center=[39, -98], zoom=4, children=[
            dl.TileLayer(),
            dl.GeoJSON(url='/assets/world_map.geojson', id="main-window-geojson",
                    options=dict(style=style_handle), 
                    hideout=BACKEND_GAME.hideout_dict_for_dash,
                    ),
        ], style={'width': '100%', 'height': '80vh'}, id="map"),
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
    country = call_country_by_name(feature["properties"]["name"])
    owner = country.owner

    to_display_string = 'ERROR'
    popup_window_is_open = False
    win_or_lose = 'ERROR'

    match BACKEND_GAME.chosen_country_1, BACKEND_GAME.chosen_country_2:
        case None, None:
            BACKEND_GAME.chosen_country_1 = country
            to_display_string = f'You have selected: {country.name} \n \
                Click on another country which you want to attack it with'
            
            # return hideout, f'You have selected: {country.name}'
        case _, None:
            BACKEND_GAME.chosen_country_2 = country
            to_display_string = f'Do you want to attack {country.name} with {BACKEND_GAME.chosen_country_1.name}? \n \
                Click again to confirm click somewhere else to go back to country selection'

        case a, b if a is not None and b is not None:
            if b == country:
                result = BACKEND_GAME.attack_backend()
                popup_window_is_open = True
                win_or_lose = result

                to_display_string = f'It\'s {BACKEND_GAME.active_player.name}\'s turn to attack'
                
            else:
                BACKEND_GAME.chosen_country_1 = None
                BACKEND_GAME.chosen_country_2 = None
                to_display_string = f'It\'s {BACKEND_GAME.active_player.name}\'s turn to attack'

    
    hideout = BACKEND_GAME.hideout_dict_for_dash
    print(f"hideout: {hideout}")
    if BACKEND_GAME.chosen_country_1:
        hideout["selected"] = [BACKEND_GAME.chosen_country_1.name, BACKEND_GAME.chosen_country_2.name] if BACKEND_GAME.chosen_country_2 else [BACKEND_GAME.chosen_country_1.name]
    else:
        hideout["selected"] = []
    
    return hideout, to_display_string, popup_window_is_open, win_or_lose

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