import dash_leaflet as dl
from dash import Dash, State, html, callback
from dash.dependencies import Output, Input
from dash_extensions.javascript import Namespace, assign, arrow_function

from country import call_country_by_name
from game_state import BACKEND_GAME, get_backend_game
from player import Player

import dash_popup_window
import dash_mantine_components as dmc

from dash_iconify import DashIconify

class MainWindow():

    def __init__(self):
        pass

def create_main_window_layout(list_of_players : list[Player]):

    ns = Namespace("myNamespace", "mySubNamespace")
    style_handle = ns('my_style')

    backend_game = get_backend_game()

    return dmc.AppShell([
        # Beautiful header section
        dmc.AppShellHeader([
            html.H1(
                "🌍 Geography Game 🗺️", 
                style={
                    'textAlign': 'center',
                #     'color': '#2c3e50',
                #     'fontSize': '3.5rem',
                #     'fontWeight': 'bold',
                #     'margin': '20px 0',
                #     'textShadow': '2px 2px 4px rgba(0,0,0,0.3)',
                #     'background': 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                #     'backgroundClip': 'text',
                #     'webkitBackgroundClip': 'text',
                #     'webkitTextFillColor': 'transparent',
                #     'fontFamily': '"Trebuchet MS", "Lucida Grande", "Lucida Sans Unicode", "Lucida Sans", Tahoma, sans-serif',
                #     'letterSpacing': '2px'
                },
                id = 'attribute-show-header',
            ),
            html.Hr(style={
                'border': 'none',
                'height': '3px',
                'background': 'linear-gradient(to right, #667eea, #764ba2)',
                'margin': '0 auto 20px auto',
                'width': '60%',
                'borderRadius': '5px'
            })
        ], style={
            'background': 'linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%)',
            'padding': '20px',
            'borderRadius': '15px',
            'marginBottom': '20px',
            'boxShadow': '0 8px 32px rgba(0,0,0,0.1)',
            'border': '1px solid rgba(255,255,255,0.2)'
        }),
        dmc.AppShellMain([
        dl.Map(center=[39, -98], zoom=4, children=[
            dl.TileLayer(),
            dl.GeoJSON(url='/assets/world_map.geojson', id="main-window-geojson",
                    options=dict(style=style_handle), 
                    hideout=backend_game.hideout_dict_for_dash,
                    hoverStyle=arrow_function(dict(weight=5, color="#666", dashArray="")),
                    ),
        ], style={'width': '100%', 'height': '100vh', 'borderRadius': '10px', 'overflow': 'hidden'}, id="map"),
        
        html.Div(id="info", style={
            'marginTop': '20px',
            'padding': '20px',
            'textAlign': 'center',
            'color': '#2c3e50',
            'fontSize': '1.5rem',
            'fontWeight': 'bold',
            'textShadow': '2px 2px 4px rgba(0,0,0,0.3)',
            'background': 'linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%)',
            'borderRadius': '15px',
            'boxShadow': '0 8px 32px rgba(0,0,0,0.1)',
            'border': '1px solid rgba(255,255,255,0.2)',
            'fontFamily': '"Trebuchet MS", "Lucida Grande", "Lucida Sans Unicode", "Lucida Sans", Tahoma, sans-serif',
            'letterSpacing': '1px',
            'minHeight': '60px',
            'display': 'flex',
            'alignItems': 'center',
            'justifyContent': 'center'
        }),
        dash_popup_window.popup_window,
    ], style={
        'padding': '20px',
        'backgroundColor': '#ffffff',
        'minHeight': '100vh',
        'fontFamily': 'Arial, sans-serif'
    }),
    dmc.Affix([
        dmc.Button(
            'Reroll',
            id='reroll-button',
            leftSection=DashIconify(icon="tabler:dice", width=20),
            size="lg",
        ),
    ],
        position={"bottom": 50, "left": 50}
    ),
    dmc.Affix(
        dmc.SegmentedControl(
            id='player-order-segmented-control',
            disabled=True,
            data = [player.name for player in list_of_players],
            value = list_of_players[0].name if list_of_players else None,
            color='blue',
            size="lg",
            orientation='vertical',
        )
    , position={"bottom": 50, "right": 50}
    ),

    dmc.AppShellFooter([
        dmc.Text("© 2025 Julius Niemeyer. All rights reserved. Built with ❤️ using Dash and Mantine.",
                  style={'textAlign': 'center', 'fontSize': '0.8rem'})
    ])
])


@callback(
    [Output("attribute-show-header", "children"),
     Output("main-window-geojson", "hideout", allow_duplicate=True),
     Output("info", "children"),
     Output("popup-window", "opened", allow_duplicate=True),
     Output("win_or_lose_title", "children"),],
    Input("main-window-geojson", "n_clicks"),
    State("main-window-geojson", "clickData"),
    State("main-window-geojson", "hideout"),
    prevent_initial_call=True,
)
def click_on_map(_, feature, hideout):
    backend_game = get_backend_game()
    country = call_country_by_name(feature["properties"]["sovereignt"])
    owner = country.owner

    to_display_string_header = 'Error'
    to_display_string = 'ERROR'
    popup_window_is_open = False
    win_or_lose = 'ERROR'
    battle_result_content = ""

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
                country_a_name = a.name if a else "Unknown"
                country_b_name = b.name if b else "Unknown"
                result = backend_game.attack_backend()
                popup_window_is_open = True
                
                # Map result strings to display messages and styling
                
                result_styling = {
                    "win": {
                        'title': "VICTORY!",
                        'message': f"{country_a_name} successfully conquered {country_b_name}!",
                        'style': {
                            'background': 'linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%)',
                            'border': '2px solid #28a745',
                            'color': '#155724'
                        }
                    },
                    "loose": {
                        'title': "DEFEAT",
                        'message': f"{country_b_name} successfully defended against {country_a_name}!",
                        'style': {
                            'background': 'linear-gradient(135deg, #f8d7da 0%, #f5c6cb 100%)',
                            'border': '2px solid #dc3545',
                            'color': '#721c24'
                        }
                    },
                    "hard defeat": {
                        'title': "CRUSHING VICTORY!",
                        'message': f"{country_a_name} completely dominated {country_b_name}!",
                        'style': {
                            'background': 'linear-gradient(135deg, #fff3cd 0%, #ffeaa7 100%)',
                            'border': '2px solid #ffc107',
                            'color': '#856404'
                        }
                    },
                    "no data": {
                        'title': "NO DATA AVAILABLE",
                        'message': "Battle cannot be resolved due to missing data for this attribute.",
                        'style': {
                            'background': 'linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%)',
                            'border': '2px solid #6c757d',
                            'color': '#495057'
                        }
                    },
                    "draw": {
                        'title': "DRAW",
                        'message': f"Both {country_a_name} and {country_b_name} are evenly matched!",
                        'style': {
                            'background': 'linear-gradient(135deg, #e2e3e5 0%, #d6d8db 100%)',
                            'border': '2px solid #6c757d',
                            'color': '#495057'
                        }
                    }
                }
                
                result_info = result_styling[result]
                win_or_lose = result_info['title']
                
                to_display_string = f'It\'s {backend_game.active_player.name}\'s turn to attack'
                
            else:
                to_display_string = f'It\'s {backend_game.active_player.name}\'s turn to attack'
                backend_game.chosen_country_1 = None
                backend_game.chosen_country_2 = None
    
    
    
    hideout = backend_game.hideout_dict_for_dash
    if backend_game.chosen_country_1:
        hideout["selected"] = [backend_game.chosen_country_1.name, backend_game.chosen_country_2.name] if backend_game.chosen_country_2 else [backend_game.chosen_country_1.name]
    else:
        hideout["selected"] = []

    return backend_game.get_replaced_A_and_B_category_string_for_current_attribute(), hideout, html.H1(to_display_string), popup_window_is_open, win_or_lose

if __name__ == "__main__":
    app = Dash(__name__)
    app.layout = create_main_window_layout()
    
    app.run(debug=True)