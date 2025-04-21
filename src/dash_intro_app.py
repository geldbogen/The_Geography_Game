import dash
from dash import dcc, html, Input, Output, State, callback
import dash_bootstrap_components as dbc
import random
import pandas as pd
import os
from player import Player
from global_definitions import all_categories
from setup_game import setup_the_game

# Initialize the Dash app with a Bootstrap theme
app = dash.Dash(__name__, 
                external_stylesheets=[dbc.themes.FLATLY],
                meta_tags=[{'name': 'viewport', 'content': 'width=device-width, initial-scale=1'}])

# Create header with game title
header = dbc.Card(
    dbc.CardBody([
        html.H1("The Geography Game", className="text-center mb-4"),
        html.H4("Set up your game and choose your options", className="text-center text-muted")
    ]), 
    className="mb-4"
)

# Player setup section
player_setup = dbc.Card([
    dbc.CardHeader(html.H4("Player Setup")),
    dbc.CardBody([
        dbc.Row([
            dbc.Col([
                dbc.Label("Player Name"),
                dbc.Input(id="player-name", placeholder="Enter your name", type="text"),
            ], width=6),
            dbc.Col([
                dbc.Label("Player Color"),
                dcc.Dropdown(
                    id='player-color',
                    options=[
                        {'label': 'Red', 'value': 'rgb(255, 0, 0)'},
                        {'label': 'Blue', 'value': 'rgb(0, 0, 255)'},
                        {'label': 'Green', 'value': 'rgb(0, 128, 0)'},
                        {'label': 'Yellow', 'value': 'rgb(255, 255, 0)'},
                        {'label': 'Purple', 'value': 'rgb(128, 0, 128)'},
                        {'label': 'Orange', 'value': 'rgb(255, 165, 0)'},
                        {'label': 'Black', 'value': 'rgb(0, 0, 0)'},
                        {'label': 'Brown', 'value': 'rgb(165, 42, 42)'},
                    ],
                    placeholder="Select a color",
                )
            ], width=6)
        ], className="mb-3"),
        dbc.Button("Add Player", id="add-player-button", color="primary", className="mr-1"),
        html.Div(id="player-list-output", className="mt-4")
    ])
], className="mb-4")

# Game settings
game_settings = dbc.Card([
    dbc.CardHeader(html.H4("Game Settings")),
    dbc.CardBody([
        dbc.Row([
            dbc.Col([
                dbc.Label("Number of Rounds"),
                dbc.Input(id="number-of-rounds", type="number", value=10, min=1),
            ], width=6),
            dbc.Col([
                dbc.Label("Starting Countries"),
                dcc.RadioItems(
                    id="start-country",
                    options=[
                        {'label': 'Random', 'value': 'random'},
                        {'label': 'Choose', 'value': 'choose'}
                    ],
                    value='random',
                    className="ms-1"
                ),
            ], width=6)
        ], className="mb-3"),
        
        dbc.Row([
            dbc.Col([
                dbc.Label("Peace Mode"),
                dbc.Checklist(
                    id="peace-mode",
                    options=[{'label': 'Enable Peace Mode', 'value': 1}],
                    value=[],
                    switch=True,
                ),
            ], width=6)
        ], className="mb-3")
    ])
], className="mb-4")

# Winning conditions
winning_conditions = dbc.Card([
    dbc.CardHeader(html.H4("Winning Conditions")),
    dbc.CardBody([
        dcc.RadioItems(
            id="winning-condition",
            options=[
                {'label': 'Number of countries', 'value': 'number of countries'},
                {'label': 'Hold 2 countries to win', 'value': 'claim 2 countries'},
                {'label': 'Claim at first the golden countries', 'value': 'get gold'},
                {'label': 'Claim countries according to a predetermined attribute', 'value': 'attribute'},
                {'label': 'Secret targets', 'value': 'secret targets'},
                {'label': 'Secret attribute', 'value': 'secret attribute'}
            ],
            value='number of countries',
            className="mb-3"
        ),
        html.Div(id="attribute-selector-container")
    ])
], className="mb-4")

# Wormhole options
wormhole_options = dbc.Card([
    dbc.CardHeader(html.H4("Wormhole Options")),
    dbc.CardBody([
        dcc.RadioItems(
            id="wormhole-option",
            options=[
                {'label': 'No wormholes at all', 'value': 'no wormholes at all'},
                {'label': 'Fixed starting wormholes', 'value': 'fixed starting wormholes'},
                {'label': 'Every round changing wormholes', 'value': 'every round changing wormholes'},
                {'label': 'Every round changing wormholes from your countries', 
                 'value': 'every round changing wormholes from your countries'}
            ],
            value='no wormholes at all'
        )
    ])
], className="mb-4")

# Continent selection
continent_selection = dbc.Card([
    dbc.CardHeader(html.H4("Choose Continents")),
    dbc.CardBody([
        dbc.Checklist(
            id="continents",
            options=[
                {'label': 'Africa', 'value': 'Africa'},
                {'label': 'North America', 'value': 'North America'},
                {'label': 'Middle America', 'value': 'Middle America'},
                {'label': 'South America', 'value': 'South America'},
                {'label': 'Asia', 'value': 'Asia'},
                {'label': 'Europe', 'value': 'Europe'},
                {'label': 'Oceania', 'value': 'Oceania'}
            ],
            value=['Africa', 'North America', 'Middle America', 'South America', 'Asia', 'Europe', 'Oceania'],
            inline=True
        )
    ])
], className="mb-4")

# Start game button
start_game_button = dbc.Button("Start Game", id="start-game", color="success", size="lg", className="w-100 mb-4")

# Layout the application with all components
app.layout = dbc.Container([
    header,
    player_setup,
    dbc.Row([
        dbc.Col(game_settings, width=6),
        dbc.Col(winning_conditions, width=6)
    ]),
    dbc.Row([
        dbc.Col(wormhole_options, width=6),
        dbc.Col(continent_selection, width=6)
    ]),
    start_game_button,
    
    # Store components to track state
    dcc.Store(id="player-list-store", data=[]),
    html.Div(id="redirect", style={"display": "none"})
], fluid=True, className="p-5")

# Callback for showing attribute selector when attribute condition is selected
@callback(
    Output("attribute-selector-container", "children"),
    Input("winning-condition", "value"),
)
def show_attribute_selector(winning_condition):
    if winning_condition == "attribute":
        # Get attribute list from all_categories
        displayed_list = [c.name for c in all_categories]
        displayed_list.sort()
        displayed_list = ["Surprise Me!"] + displayed_list
        displayed_list = [m.rstrip(".csv") for m in displayed_list]
        
        options = [{'label': attr, 'value': attr} for attr in displayed_list]
        
        return html.Div([
            dbc.Row([
                dbc.Col([
                    dbc.Label("Select Attribute"),
                    dcc.Dropdown(
                        id="end-attribute",
                        options=options,
                        value=displayed_list[0],
                        clearable=False
                    ),
                ], width=8),
                dbc.Col([
                    dbc.Label("Reverse?"),
                    dbc.Checklist(
                        id="reverse-attribute",
                        options=[{'label': 'Yes', 'value': 1}],
                        value=[],
                        switch=True
                    ),
                ], width=4),
            ]),
            dbc.Button("Randomize", id="randomize-attribute", color="secondary", className="mt-2")
        ])
    return []

# Callback for randomizing attribute
@callback(
    [Output("end-attribute", "value"),
     Output("reverse-attribute", "value")],
    Input("randomize-attribute", "n_clicks"),
    State("end-attribute", "options"),
    prevent_initial_call=True
)
def randomize_attribute(n_clicks, options):
    if not n_clicks:
        return dash.no_update, dash.no_update
    
    # Skip first option which is "Surprise Me!"
    rng = random.randrange(1, len(options))
    reverse = [1] if random.random() <= 0.5 else []
    
    return options[rng]['value'], reverse

# Callback to add players and update player list
@callback(
    [Output("player-list-output", "children"),
     Output("player-list-store", "data"),
     Output("player-name", "value"),
     Output("player-color", "value")],
    [Input("add-player-button", "n_clicks")],
    [State("player-name", "value"),
     State("player-color", "value"),
     State("player-list-store", "data")],
    prevent_initial_call=True
)
def add_player(n_clicks, name, color, current_players):
    if not n_clicks or not name or not color:
        return dash.no_update, dash.no_update, dash.no_update, dash.no_update
    
    # Add new player to list
    current_players.append({"name": name, "color": color})
    
    # Create table to display players
    table_header = [html.Thead(html.Tr([html.Th("Name"), html.Th("Color")]))]
    
    table_body = [html.Tbody([
        html.Tr([
            html.Td(player["name"]),
            html.Td(html.Div(style={"height": "20px", "width": "20px", "backgroundColor": player["color"], "borderRadius": "50%"}))
        ]) for player in current_players
    ])]
    
    table = dbc.Table(table_header + table_body, bordered=True)
    
    return table, current_players, "", None

# Callback to handle game start
@callback(
    Output("redirect", "children"),
    Input("start-game", "n_clicks"),
    [State("player-list-store", "data"),
     State("number-of-rounds", "value"),
     State("start-country", "value"),
     State("winning-condition", "value"),
     State("continents", "value"),
     State("wormhole-option", "value"),
     State("peace-mode", "value")],
    prevent_initial_call=True
)
def start_game(n_clicks, players, number_of_rounds, start_country, winning_condition, continents, wormhole_option, peace_mode):
    if not n_clicks or not players:
        return dash.no_update
    
    # If attribute is chosen, also get the attribute value and reverse setting
    end_attribute = "Random.csv"
    reversed_attribute = 0
    
    if winning_condition == "attribute":
        try:
            end_attribute = dash.callback_context.states["end-attribute.value"] + ".csv"
            reversed_attribute = 1 if dash.callback_context.states["reverse-attribute.value"] else 0
        except:
            pass

    # Convert the players data to Player objects
    player_objects = []
    for player in players:
        # Convert color from string to RGB tuple
        color_str = player["color"].strip("rgb(").strip(")").split(",")
        color = tuple(int(c.strip()) for c in color_str)
        player_objects.append(Player(color=color, name=player["name"]))
    
    # Call setup_the_game with all parameters
    setup_the_game(
        continent_list=continents,
        list_of_players=player_objects,
        number_of_rounds=number_of_rounds,
        number_of_rerolls=number_of_rounds // 3,
        starting_countries_preferences=start_country,
        winning_condition=winning_condition,
        end_attribute_path=end_attribute,
        peacemode=bool(peace_mode),
        wormhole_mode=wormhole_option,
        reversed_end_attribute=reversed_attribute,
        start_the_game=True
    )
    
    # This will close the Dash app
    return dcc.Location(pathname="/", id="close-app")

def run_dash_app():
    app.run(debug=True)

if __name__ == "__main__":
    run_dash_app()
