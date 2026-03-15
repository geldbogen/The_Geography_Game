import dash
import dash_leaflet as dl
from dash import Dash, State, html, callback
from dash.dependencies import Output, Input
from dash_extensions.javascript import Namespace, assign, arrow_function

from country import call_country_by_name
from error_handler import ErrorHandler
from game_state import BACKEND_GAME, get_backend_game
from player import Player

import dash_popup_window
import dash_mantine_components as dmc

from dash_iconify import DashIconify


class MainWindow():

    def __init__(self):
        pass


def create_main_window_layout(list_of_players : list[Player], number_of_rounds : int = 10):

    ns = Namespace("myNamespace", "mySubNamespace")
    style_handle = ns('my_style')

    backend_game = get_backend_game()

    return dmc.AppShell([
        # Beautiful header section
        dmc.AppShellHeader([
            dmc.Title(
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
            dmc.Divider(
            )
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
            dl.TileLayer(url='https://server.arcgisonline.com/ArcGIS/rest/services/Canvas/World_Light_Gray_Base/MapServer/tile/{z}/{y}/{x}',
            attribution='Tiles &copy; Esri &mdash; Esri, DeLorme, NAVTEQ',
            noWrap=True),
            dl.GeoJSON(url='/assets/world_map.geojson', id="main-window-geojson",
                    options=dict(style=style_handle), 
                    hideout=backend_game.hideout_dict_for_dash,
                    hoverStyle=arrow_function(dict(weight=5, color="#666", dashArray="")),
                    ),
        ], style={'width': '100%', 'height': '100vh', 'overflow': 'hidden', 'expand': True}, id="map"),

        dash_popup_window.popup_window,
        dmc.NotificationContainer(
            id='notification-container',

            ),
    
    dmc.Affix([
        dmc.Button(
            f'Rerolls left: {number_of_rounds // 3}',
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
            data = [f'Round: 1 / {number_of_rounds}'] + [player.name for player in list_of_players],
            value = list_of_players[0].name if list_of_players else None,
            color='blue',
            size="lg",
        )
    , position={"bottom": 50, "right": 50}
    ),

    ],
    style={
        'padding': '20px',
        'backgroundColor': '#ffffff',
        'minHeight': '100vh',
        'fontFamily': 'Arial, sans-serif'
    }),
    
    
    dmc.AppShellFooter([
        dmc.Text("© 2026 Julius Niemeyer. All rights reserved. Built with ❤️ using Dash and Mantine.",
                  style={'textAlign': 'center', 'fontSize': '0.8rem'})
    ])
])


@callback(
    [Output("attribute-show-header", "children"),
     Output("main-window-geojson", "hideout", allow_duplicate=True),
     Output("popup-window", "opened", allow_duplicate=True),
     Output("win_or_lose_title", "children"),
     Output("notification-container", "sendNotifications")
     ],
    Input("main-window-geojson", "n_clicks"),
    State("main-window-geojson", "clickData"),
    State("main-window-geojson", "hideout"),
    State("popup-window", "opened"),
    prevent_initial_call=True,
)
def click_on_map(_, feature, hideout, popup_is_open):
    backend_game = get_backend_game()

    if getattr(backend_game, "ignore_next_map_click", False):
        backend_game.ignore_next_map_click = False
        return dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update

    if popup_is_open or not feature:
        return dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update
    print(f'countryname clicked: {feature["properties"]["sovereignt"]}')
    country = call_country_by_name(feature["properties"]["sovereignt"])
    owner = country.owner

    to_display_string_header = 'Error'
    to_display_string = 'ERROR'
    battle_result_content = ""
    popup_window_is_open = False
    win_or_lose = 'ERROR'

    match backend_game.chosen_country_1, backend_game.chosen_country_2:
        case None, None:
            notifications = ErrorHandler.invalid_attacker_notifications(backend_game, country)
            if notifications:
                return dash.no_update, dash.no_update, dash.no_update, dash.no_update, notifications
            backend_game.chosen_country_1 = country

        case _, None:
            is_valid_selection, notifications, should_clear_attacker = ErrorHandler.validate_second_country_selection(
                backend_game, country
            )
            if is_valid_selection:
                backend_game.chosen_country_2 = country
            else:
                if should_clear_attacker:
                    backend_game.chosen_country_1 = None
                hideout = ErrorHandler.sync_selected_countries(backend_game, backend_game.hideout_dict_for_dash)
                return (
                    backend_game.get_replaced_A_and_B_category_string_for_current_attribute(),
                    hideout,
                    dash.no_update,
                    dash.no_update,
                    notifications,
                )

        case a, b if a is not None and b is not None:
            if b == country:
                
                # attack function triggered
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
                
            else:
                backend_game.chosen_country_1 = None
                backend_game.chosen_country_2 = None
    
    
    
    hideout = backend_game.hideout_dict_for_dash
    hideout = ErrorHandler.sync_selected_countries(backend_game, hideout)

    return backend_game.get_replaced_A_and_B_category_string_for_current_attribute(), hideout, popup_window_is_open, win_or_lose, []



@callback(
    Output("attribute-show-header", "children", allow_duplicate=True),
    Output("reroll-button", "children", allow_duplicate=True),
    Input("reroll-button", "n_clicks"),
    prevent_initial_call=True,
)
def click_reroll_button(n_clicks):
    backend_game = get_backend_game()
    if n_clicks:
        if backend_game.active_player.rerolls_left == 0:
            return dash.no_update, dash.no_update
        else:
            backend_game.roll_a_new_attribute(backend_game.active_player, pressed_reroll_button=True)
            return backend_game.get_replaced_A_and_B_category_string_for_current_attribute(), f'Rerolls left: {backend_game.active_player.rerolls_left}'



