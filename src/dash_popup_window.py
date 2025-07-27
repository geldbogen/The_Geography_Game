import dash_leaflet as dl
from dash import Dash, State, html, callback
from dash.dependencies import Output, Input
from dash_extensions.javascript import Namespace, assign


import dash_bootstrap_components as dbc
import dash_mantine_components as dmc

from game_state import get_backend_game
from dash_popup_extra_information_card import get_two_popup_extra_information_window_cards


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
    html.Div([
        # Country vs Country display
        html.Div([
            html.Div([
                html.H4("Attacking Country", style={
                    'textAlign': 'center',
                    'color': '#e74c3c',
                    'fontWeight': 'bold',
                    'marginBottom': '10px'
                }),
                html.Div(id="country-a-info", style={
                    'padding': '15px',
                    'background': 'linear-gradient(135deg, #ffecec 0%, #ffd6d6 100%)',
                    'borderRadius': '10px',
                    'border': '2px solid #e74c3c',
                    'textAlign': 'center'
                })
            ], style={'width': '45%'}),
            
            html.Div([
                html.H3("VS", style={
                    'textAlign': 'center',
                    'color': '#34495e',
                    'fontWeight': 'bold',
                    'fontSize': '2rem',
                    'margin': '20px 0'
                })
            ], style={'width': '10%', 'display': 'flex', 'alignItems': 'center', 'justifyContent': 'center'}),
            
            html.Div([
                html.H4("Defending Country", style={
                    'textAlign': 'center',
                    'color': '#3498db',
                    'fontWeight': 'bold',
                    'marginBottom': '10px'
                }),
                html.Div(id="country-b-info", style={
                    'padding': '15px',
                    'background': 'linear-gradient(135deg, #ebf4ff 0%, #d6e9ff 100%)',
                    'borderRadius': '10px',
                    'border': '2px solid #3498db',
                    'textAlign': 'center'
                })
            ], style={'width': '45%'})
        ], style={
            'display': 'flex',
            'justifyContent': 'space-between',
            'alignItems': 'flex-start',
            'marginBottom': '20px'
        }),
        
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
        
    ], style={
        'padding': '20px',
        'background': 'linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%)'
    }),

    html.Div(id='extra-information-cards'),

    # Modal Footer with close button
  
    dmc.Button(
        "Continue Game", 
        id="close-button",
        size="lg",
    )
])


popup_window = dmc.Modal(
    children=pop_up_window_content,
    id="popup-window",
    size="lg",
    centered=True,
    opened=False,
)

# Callback to populate popup content when it opens
@callback(
    [Output("country-a-info", "children"),
     Output("country-b-info", "children"),
     Output("attribute-info", "children"),
     Output("extra-information-cards", "children")],
    Input("popup-window", "opened", ),
    prevent_initial_call=True
)
def populate_popup_content(is_open):
    if not is_open:
        return "", "", "", ""
    
    backend_game = get_backend_game()
    
    if not backend_game.chosen_country_1 or not backend_game.chosen_country_2:
        return "", "", "", ""

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
            html.P(f"World Rank: {displayed_world_rank_a}", style={'margin': '5px 0'}),
            html.P(f"(of {displayed_how_many_ranked_a} ranked)", style={'margin': '5px 0', 'fontSize': '0.9rem'})
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
        
        country_b_info = html.Div([
            html.H5(country_b.name, style={'fontWeight': 'bold', 'marginBottom': '10px'}),
            html.P(f"Value: {formatted_value_b}", style={'margin': '5px 0'}),
            html.P(f"World Rank: {displayed_world_rank_b}", style={'margin': '5px 0'}),
            html.P(f"(of {displayed_how_many_ranked_b} ranked)", style={'margin': '5px 0', 'fontSize': '0.9rem'})
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

    first_image_path = "assets/pictures/attribute_pictures/" + current_attribute.name.replace(
                    ".csv", "") + "/" + country_a.dict_of_attributes[
                        current_attribute.name].additional_information_name + ".jpg"

    second_image_path = "assets/pictures/attribute_pictures/" + current_attribute.name.replace(
                    ".csv", "") + "/" + country_b.dict_of_attributes[
                        current_attribute.name].additional_information_name + ".jpg"

    extra_information_two_window_content = get_two_popup_extra_information_window_cards(
        first_image_path, first_wiki_info_name, first_wiki_info, first_wiki_link,
        second_image_path, second_wiki_info_name, second_wiki_info, second_wiki_link
    )

    if first_wiki_info_name == '' and second_wiki_info_name == '':
        extra_information_two_window_content = ""
    return country_a_info, country_b_info, attribute_info, extra_information_two_window_content

# Callback to close popup
@callback(
    Output("popup-window", "opened", allow_duplicate=True),
    Output("main-window-geojson", "hideout", allow_duplicate=True),
    Input("close-button", "n_clicks"),
    State("popup-window", "opened"),
    State("main-window-geojson", "hideout"),
    prevent_initial_call=True
)
def close_popup(n_clicks, is_open, hideout):
    if n_clicks:
        hideout['selected'] = []
        backend_game = get_backend_game()
        # Reset the chosen countries after battle
        # do transition
        
        game_should_end = backend_game.go_to_next_turn_and_check_if_game_should_end()
        if game_should_end:
            pass
            # do endscreen later

        return False, hideout
    return is_open, hideout