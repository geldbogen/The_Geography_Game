import json
import dash
import dash_leaflet as dl
from dash import Dash, State, html, callback, ALL, callback_context
from dash.dependencies import Output, Input
from dash_extensions.javascript import Namespace, assign


import dash_bootstrap_components as dbc
import dash_mantine_components as dmc

from game_state import get_backend_game
from dash_popup_extra_information_card import get_two_popup_extra_information_window_cards
from dash_iconify import DashIconify

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
        ], style={'marginBottom': '20px'}),

        dmc.Grid([
            dmc.GridCol([
                html.Div(id="country-a-info", style={
                    'padding': '15px',
                    'borderRadius': '10px',
                    'border': '2px solid #e74c3c',
                    'textAlign': 'center'
                }),
                html.Div(id="country-a-info-card",)
            ],
            span=6),

            dmc.GridCol([
                html.Div(id="country-b-info", style={
                    'padding': '15px',
                    'borderRadius': '10px',
                    'border': '2px solid #3498db',
                    'textAlign': 'center'
                }),
                html.Div(id="country-b-info-card",)
            ],
            span=6)
        ],
        ),
        

    # Modal Footer with close button
    dmc.Group(id='footer-buttons', children=[
        dmc.Button(
            "Continue Game", 
            id={"type": "close-button", "is_guessed_correct_or_not": "not_guessed_correct"},
            size="lg",
            justify="flex-end",

        ),        
    ],
    style={'padding': '20px', 'textAlign': 'center', 'background': 'linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%)', 'borderRadius': '0 0 15px 15px', 'border': 'none'}
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
    
    # Country A information
    try:
        displayed_world_rank_a = str(
            country_a.dict_of_attributes[current_attribute.name].rank) if country_a.dict_of_attributes[current_attribute.name].rank != 0 else "--"
        displayed_how_many_ranked_a = str(
            country_a.dict_of_attributes[current_attribute.name].number_of_countries_ranked) if country_a.dict_of_attributes[current_attribute.name].number_of_countries_ranked != 1 else "--"
        
        value_a = country_a.dict_of_attributes[current_attribute.name].value
        formatted_value_a = format(value_a, ",") if value_a != -1.0 else "--"
        
        country_a_info = html.Div([
            html.H5(country_a.name, style={'fontWeight': 'bold', 'marginBottom': '10px'}),
            html.P(f"Value: {formatted_value_a}", style={'margin': '5px 0'}),
            html.P(f"World Rank: #{displayed_world_rank_a} / {displayed_how_many_ranked_a}", style={'margin': '5px 0'}),
        ])
    except:
        country_a_info = html.Div([
            html.H5(country_a.name, style={'fontWeight': 'bold', 'marginBottom': '10px'}),
            html.P("No data available", style={'margin': '5px 0'})
        ])
    
    # Country B information
    try:
        displayed_world_rank_b = str(
            country_b.dict_of_attributes[current_attribute.name].rank) if country_b.dict_of_attributes[current_attribute.name].rank != 0 else "--"
        displayed_how_many_ranked_b = str(
            country_b.dict_of_attributes[current_attribute.name].number_of_countries_ranked) if country_b.dict_of_attributes[current_attribute.name].number_of_countries_ranked != 1 else "--"
        
        value_b = country_b.dict_of_attributes[current_attribute.name].value
        formatted_value_b = format(value_b, ",") if value_b != -1.0 else "--"
        print('This is the country code: ')
        print(country_b.get_two_country_code())
        country_b_info = html.Div([
            dmc.Image(src=f'/assets/pictures/flag_pictures/w1280/{country_b.get_two_country_code()}.png', radius='50%'),
            html.H5(country_b.name, style={'fontWeight': 'bold', 'marginBottom': '10px'}),
            html.P(f"Value: {formatted_value_b}", style={'margin': '5px 0'}),
            html.P(f"World Rank: #{displayed_world_rank_b} / {displayed_how_many_ranked_b}", style={'margin': '5px 0'}),
        ])
    except:
        country_b_info = html.Div([
            html.H5(country_b.name, style={'fontWeight': 'bold', 'marginBottom': '10px'}),
            html.P("No data available", style={'margin': '5px 0'})
        ])
    
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
        
        hideout['selected'] = []
        backend_game = get_backend_game()
        # Reset the chosen countries after battle
        # do transition

        game_should_end = backend_game.go_to_next_turn_and_check_if_game_should_end(same_player_again=same_player_again)
        if game_should_end:
            pass
            # do endscreen later

        segmented_control_data[0] = f'Round: {backend_game.which_round_counter + 1} / {backend_game.number_of_rounds}' 
        to_display_string = backend_game.get_replaced_A_and_B_category_string_for_current_attribute()

        return False, hideout, backend_game.active_player.name, segmented_control_data, to_display_string
    return is_open, hideout, dash.no_update, dash.no_update, dash.no_update
