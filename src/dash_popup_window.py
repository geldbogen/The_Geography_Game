import json
import dash
import dash_leaflet as dl
from dash import Dash, State, html, callback, ALL, callback_context
from dash.dependencies import Output, Input
from dash_extensions.javascript import Namespace, assign


import dash_bootstrap_components as dbc
import dash_mantine_components as dmc

from game_logging import get_game_logger
from game_state import get_backend_game
from dash_popup_extra_information_card import get_two_popup_extra_information_window_cards
from dash_iconify import DashIconify


LOGGER = get_game_logger("dash_popup_window")


def _get_flag_asset_path(country) -> str:
    country_code = country.get_two_country_code().lower()
    return f"/assets/pictures/flag_pictures/w320/{country_code}.png"


def _build_country_info(country, current_attribute, accent_color: str):
    try:
        local_attribute = country.dict_of_attributes[current_attribute.name]
        displayed_world_rank = str(local_attribute.rank) if local_attribute.rank != 0 else "--"
        displayed_how_many_ranked = (
            str(local_attribute.number_of_countries_ranked)
            if local_attribute.number_of_countries_ranked != 1 else "--"
        )
        formatted_value = format(local_attribute.value, ",") if local_attribute.value != -1.0 else "--"
        details = [
            html.P(f"Value: {formatted_value}", style={'margin': '4px 0', 'fontSize': '1rem'}),
            html.P(
                f"World Rank: #{displayed_world_rank} / {displayed_how_many_ranked}",
                style={'margin': '4px 0', 'fontSize': '1rem'},
            ),
        ]
    except Exception:
        details = [html.P("No data available", style={'margin': '4px 0', 'fontSize': '1rem'})]

    return html.Div(
        [
            html.H5(country.name, style={'fontWeight': 'bold', 'marginBottom': '8px', 'minHeight': '3rem'}),
            html.Div(
                dmc.Image(
                    src=_get_flag_asset_path(country),
                    fallbackSrc='/assets/pictures/flag_pictures/w320/noflag.png',
                    fit="contain",
                    h=72,
                    w=116,
                    radius="sm",
                ),
                style={
                    'width': '116px',
                    'height': '72px',
                    'display': 'flex',
                    'alignItems': 'center',
                    'justifyContent': 'center',
                    'marginBottom': '14px',
                    'borderRadius': '10px',
                    'overflow': 'hidden',
                    'background': 'linear-gradient(180deg, #f8fafc 0%, #eef2f7 100%)',
                    'boxShadow': 'inset 0 0 0 1px rgba(148, 163, 184, 0.25)',
                },
            ),
            html.Div(details),
        ],
        style={
            'padding': '18px',
            'borderRadius': '14px',
            'border': f'2px solid {accent_color}',
            'background': 'linear-gradient(180deg, rgba(255,255,255,0.98) 0%, rgba(245,247,250,0.92) 100%)',
            'textAlign': 'center',
            'minHeight': '220px',
            'display': 'flex',
            'flexDirection': 'column',
            'justifyContent': 'center',
            'alignItems': 'center',
            'boxShadow': '0 10px 24px rgba(0,0,0,0.08)',
        },
    )

pop_up_window_content = html.Div([
    # Modal Header with beautiful styling
    html.Div([
        html.H2("", id='win_or_lose_title', style={
            'textAlign': 'center',
            'color': '#2c3e50',
            'fontSize': '2.5rem',
            'fontWeight': 'bold',
            'margin': '0',
            'textShadow': '2px 2px 4px rgba(0,0,0,0.3)',
            'background': 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
            'backgroundClip': 'text',
            'webkitBackgroundClip': 'text',
            'webkitTextFillColor': 'transparent',
            'fontFamily': '"Trebuchet MS", "Lucida Grande", "Lucida Sans Unicode", "Lucida Sans", Tahoma, sans-serif',
            'letterSpacing': '2px'
        })
    ], style={
        'background': 'linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%)',
        'borderRadius': '15px 15px 0 0',
        'padding': '20px',
        'border': 'none'
    }),
    
    # Modal Body with country information and battle details
    dmc.Container([
        # Country vs Country display
        
        # Attribute information
        html.Div([
            html.H4("Battle Attribute", style={
                'textAlign': 'center',
                'color': '#8e44ad',
                'fontWeight': 'bold',
                'marginBottom': '15px'
            }),
            html.Div(id="attribute-info", style={
                'padding': '15px',
                'background': 'linear-gradient(135deg, #f3e7ff 0%, #e7d6ff 100%)',
                'borderRadius': '10px',
                'border': '2px solid #8e44ad',
                'textAlign': 'center',
                'fontWeight': 'bold',
                'fontSize': '1.2rem'
            })
        ], style={'marginBottom': '28px'}),

        dmc.Grid([
            dmc.GridCol([
                html.Div(id="country-a-info", style={
                    'padding': '15px',
                    'borderRadius': '10px',
                    'border': '2px solid #e74c3c',
                    'textAlign': 'center'
                }),
                html.Div(id="country-a-info-card", style={'marginTop': '18px'})
            ],
            span=6),

            dmc.GridCol([
                html.Div(id="country-b-info", style={
                    'padding': '15px',
                    'borderRadius': '10px',
                    'border': '2px solid #3498db',
                    'textAlign': 'center'
                }),
                html.Div(id="country-b-info-card", style={'marginTop': '18px'})
            ],
            span=6)
        ],
        gutter="xl",
        ),
        

    # Modal Footer with close button
    dmc.Group(id='footer-buttons', children=[
            dmc.Button(
                "Continue Game", 
                id={"type": "close-button", "is_guessed_correct_or_not": "not_guessed_correct"},
                size="lg",
                justify="center",
                variant="filled",
            ),        
    ],
    justify='center',
    style={'padding': '20px', 'textAlign': 'center', 'background': 'linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%)', 'borderRadius': '0 0 15px 15px', 'border': 'none', 'width': '100%'}
    )
    
    ], style={
        'padding': '20px',
        'background': 'linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%)'
    }),
])


popup_window = dmc.MantineProvider(dmc.Modal(
    children=pop_up_window_content,
    id="popup-window",
    size="60%",
    centered=True,
    opened=False,
)
)
# Callback to populate popup content when it opens
@callback(
    [Output("country-a-info", "children"),
     Output("country-b-info", "children"),
     Output("attribute-info", "children"),
     Output("country-a-info-card", "children"),
     Output("country-b-info-card", "children"),
     Output('footer-buttons', 'children')
    ],
    Input("popup-window", "opened", ),
    State('footer-buttons', 'children'),
    prevent_initial_call=True
)
def populate_popup_content(is_open, footer_buttons_content):
    if not is_open:
        return "", "", "", "", '', footer_buttons_content

    backend_game = get_backend_game()
    
    if not backend_game.chosen_country_1 or not backend_game.chosen_country_2:
        return "", "", "", "", "", footer_buttons_content

    country_a = backend_game.chosen_country_1
    country_b = backend_game.chosen_country_2
    current_attribute = backend_game.current_attribute
    
    country_a_info = _build_country_info(country_a, current_attribute, '#e74c3c')
    country_b_info = _build_country_info(country_b, current_attribute, '#3498db')
    
    # Attribute information
    attribute_info = current_attribute.name.replace(".csv", "")
    
    # get maybe the extra information
    first_wiki_info_name = country_a.dict_of_attributes[current_attribute.name].additional_information_name
    second_wiki_info_name = country_b.dict_of_attributes[current_attribute.name].additional_information_name

    first_wiki_info = country_a.dict_of_attributes[current_attribute.name].additional_information
    second_wiki_info = country_b.dict_of_attributes[current_attribute.name].additional_information

    first_wiki_link = country_a.dict_of_attributes[current_attribute.name].additional_information_link
    second_wiki_link = country_b.dict_of_attributes[current_attribute.name].additional_information_link

    first_image_path = "/assets/pictures/attribute_pictures/" + current_attribute.name.replace(
                    ".csv", "") + "/" + country_a.dict_of_attributes[
                        current_attribute.name].additional_information_name + ".jpg"

    second_image_path = "/assets/pictures/attribute_pictures/" + current_attribute.name.replace(
                    ".csv", "") + "/" + country_b.dict_of_attributes[
                        current_attribute.name].additional_information_name + ".jpg"

    extra_information_two_window_content = get_two_popup_extra_information_window_cards(
        first_image_path, first_wiki_info_name, first_wiki_info, first_wiki_link,
        second_image_path, second_wiki_info_name, second_wiki_info, second_wiki_link
    )
    if backend_game.current_attribute.is_active:
        guessed_correct_button = dmc.Button(
            "Guessed Correct",
            id = {"type": "close-button", "is_guessed_correct_or_not": "guessed_correct"},
            size="lg",
            justify="center",
            variant="filled",
        )
        footer_buttons_content = [guessed_correct_button]

    if first_wiki_info_name == '' and second_wiki_info_name == '':
        extra_information_two_window_content = ["", ""]
    return country_a_info, country_b_info, attribute_info, extra_information_two_window_content[0], extra_information_two_window_content[1], footer_buttons_content

# Callback to close popup
@callback(
    Output("popup-window", "opened", allow_duplicate=True),
    Output("main-window-geojson", "hideout", allow_duplicate=True),
    Output('player-order-segmented-control', 'value', allow_duplicate=True),
    Output('player-order-segmented-control', 'data', allow_duplicate=True),
    Output('attribute-show-header', 'children', allow_duplicate=True),
    Input({"type": "close-button", "is_guessed_correct_or_not": ALL}, "n_clicks"),
    State('player-order-segmented-control', 'data'),
    State("popup-window", "opened"),
    State("main-window-geojson", "hideout"),
    prevent_initial_call=True
)
def close_popup(n_clicks, segmented_control_data, is_open, hideout):

    print(f"Close popup called with n_clicks: {n_clicks}")
    if callback_context.triggered and callback_context.triggered[0]['value']:
        triggered_prop_id = callback_context.triggered[0]['prop_id']
        button_id_string = triggered_prop_id.split('.')[0]
        
        # Convert string back to dictionary
        button_id = json.loads(button_id_string)
        
        # Get which country was guessed
        same_player_again = (button_id["is_guessed_correct_or_not"] == 'guessed_correct')  
        LOGGER.info(
            "popup_closed | same_player_again=%s | previous_active_player=%s",
            same_player_again,
            getattr(get_backend_game().active_player, "name", None),
        )
        
        hideout['selected'] = []
        backend_game = get_backend_game()
        backend_game.ignore_next_map_click = True
        # Reset the chosen countries after battle
        # do transition

        game_should_end = backend_game.go_to_next_turn_and_check_if_game_should_end(same_player_again=same_player_again)
        if game_should_end:
            LOGGER.info("popup_transition_completed | game_should_end=True")
            pass
            # do endscreen later
        else:
            LOGGER.info(
                "popup_transition_completed | game_should_end=False | next_active_player=%s | round=%s",
                backend_game.active_player.name,
                backend_game.which_round_counter + 1,
            )

        segmented_control_data[0] = f'Round: {backend_game.which_round_counter + 1} / {backend_game.number_of_rounds}' 
        to_display_string = backend_game.get_replaced_A_and_B_category_string_for_current_attribute()

        return False, hideout, backend_game.active_player.name, segmented_control_data, to_display_string
    return is_open, hideout, dash.no_update, dash.no_update, dash.no_update
