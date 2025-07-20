import dash
import dash_leaflet as dl
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State
import json

# 1. SETUP
# Load the country border data from your GeoJSON file
with open("world_map.geojson", "r") as f:
    geojson_data = json.load(f)

# Create the Dash App
app = dash.Dash(__name__)

# This dictionary acts as our game state database
initial_owners = {feature['properties']['ADMIN']: None for feature in geojson_data['features']}

# 2. LAYOUT DEFINITION
app.layout = html.Div([
    html.H1("World Domination Game"),
    # The interactive map component
    dl.Map(center=[20, 0], zoom=2, children=[
        dl.TileLayer(),
        # The GeoJSON layer that displays the countries
        dl.GeoJSON(data=geojson_data, id="countries-layer", hoverStyle=dict(weight=5, color='#666', dashArray=''))
    ], style={'width': '100%', 'height': '80vh'}),

    # A hidden component to store our game state (the dictionary of owners)
    dcc.Store(id='game-state', data=initial_owners)
])

# 3. INTERACTIVITY CALLBACK
@app.callback(
    Output('countries-layer', 'data'),      # The map layer will be our output
    Output('game-state', 'data'),           # We also update the stored game state
    Input('countries-layer', 'click_feature'), # The trigger is a click on a country feature
    State('game-state', 'data')             # We get the current state without triggering the callback
)
def claim_country(feature, current_owners):
    # If nothing has been clicked yet, don't do anything
    if feature is None:
        return dash.no_update, dash.no_update

    # Get the name of the clicked country
    country_name = feature['properties']['ADMIN']
    print(f"Clicked on {country_name}")

    # --- Game Logic ---
    # If the country is unowned, claim it for 'blue'
    if current_owners[country_name] is None:
        current_owners[country_name] = 'blue'
        print(f"{country_name} has been claimed by blue!")

    # --- Update the Map's Visuals ---
    # We need to add a 'style' dictionary to each country based on its owner
    for feat in geojson_data['features']:
        owner = current_owners[feat['properties']['ADMIN']]
        if owner == 'blue':
            feat['properties']['style'] = {'fillColor': 'blue', 'color': 'white', 'weight': 2}
        else:
            feat['properties']['style'] = {'fillColor': 'grey', 'color': 'white', 'weight': 1}

    # Return the updated map data and the updated game state
    return geojson_data, current_owners

if __name__ == '__main__':
    app.run_server(debug=True)