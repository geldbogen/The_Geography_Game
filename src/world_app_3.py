from dash import Dash, html, dcc, callback, Output, Input
import dash
import dash_bootstrap_components as dbc
import dash_leaflet as dl
# import dash_html_components as html
# import dash_core_components as dcc
from dash.dependencies import Input, Output, State
import json
from dash_extensions.javascript import assign

# 1. SETUP
# Load the country border data from your GeoJSON file
with open("world_map.geojson", "r", encoding='utf-8') as f:
    geojson_data = json.load(f)

# Create the Dash App
app = Dash(__name__)

# This dictionary acts as our game state database
initial_owners = {feature['properties']['sovereignt']: None for feature in geojson_data['features']}

style_handle = assign("""function(feature, context){
    const match = context.props.hideout &&  context.props.hideout.properties.name === feature.properties.name;
    if(match) return {color:'#126'};
    return {}
    }""")

# 2. LAYOUT DEFINITION
app.layout = html.Div([
    html.H1("World Domination Game"),
    # The interactive map component
    dl.Map(center=[20, 0], zoom=2, children=[
        dl.TileLayer(),
        # The GeoJSON layer that displays the countries
        dl.GeoJSON(data=geojson_data, 
                   id="countries-layer",
                     hoverStyle=dict(weight=5, color='#666', dashArray=''),
                     options=dict(style=style_handle),
                     hideout=dict(selected=[])
                     ),
    ], style={'width': '100%', 'height': '80vh'}),
    html.Div(id='countries-container', children=[]),
    dash.dash_table.DataTable(id='countries-table', columns=[{"name": i, "id": i} for i in ["state"]], data=[]),


    # A hidden component to store our game state (the dictionary of owners)
    dcc.Store(id='game-state', data=initial_owners)
])

# 3. INTERACTIVITY CALLBACK
app.clientside_callback(
    """
    function(clickedFeature, hideout) {
        if (!clickedFeature) {
            // NB. raise PreventUpdate to prevent ALL outputs updating, 
            // dash.no_update prevents only a single output updating
            throw window.dash_clientside.PreventUpdate;
        }

        const id = clickedFeature.id;
        const selection = hideout || {};

        if (id in selection) {
            delete selection[id];
        }
        else {
            selection[id] = clickedFeature;
        }

        const stateText = `Clicked: ${clickedFeature.properties.NAME}`;

        return [selection, tableData, stateText, null];
    }
    """,
    Output("countries-layer", "hideout"),
    Output("countries-table", "data"),
    Output("countries-container", "children"),
    Output("countries-layer", "click_feature"),
    Input("countries-layer", "click_feature"),
    State("countries-layer", "hideout")
)

if __name__ == '__main__':
    app.run(debug=True)