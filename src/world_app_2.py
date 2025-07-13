from dash import Dash, dcc, html, Input, Output, State
import plotly.express as px
import plotly.graph_objects as go
import json

with open('src/world_map.geojson', 'r', encoding='utf-8') as f:
    geojson_data = json.load(f)

app = Dash(__name__)

app.layout = html.Div([
    html.H4('Polotical candidate voting pool analysis'),
    html.P("Select a candidate:"),
    dcc.RadioItems(
        id='candidate',
        options=["Joly", "Coderre", "Bergeron"],
        value="Coderre",
        inline=True
    ),
    dcc.Graph(id="graph"),
    html.Div(id='click-info',
              style={'margin-top': '20px', 
                     'padding': '10px', 
                     'border': '1px solid #ccc'}),
    dcc.Store(id='selected-country', data=None)
])


# @app.callback(
#     Output("graph", "figure"),
#     Input("candidate", "value"))
# def display_choropleth(candidate):

#     fig = px.choropleth_map(
#         geojson=geojson_data)
#     fig.update_layout(
#         margin={"r":0,"t":0,"l":0,"b":0})

#     return fig

@app.callback(
    [Output("graph", "figure"),
     Output("selected-country", "data")],
    [Input("candidate", "value"),
     Input("graph", "clickData")],
    [State("selected-country", "data")]
)
def update_map_and_selection(candidate, clickData, current_selection):
    # Determine which country was clicked
    selected_country = current_selection
    if clickData:
        point = clickData['points'][0]
        # Extract country identifier from click data
        clicked_country = point.get('location', point.get('customdata', [None])[0])
        selected_country = clicked_country
    
    # Create base map
    fig = px.choropleth_mapbox(
        geojson=geojson_data,
        locations=[],  # We'll handle coloring manually
        mapbox_style="carto-positron",
        zoom=1,
        center={"lat": 0, "lon": 0}
    )
    
    # Add countries with custom coloring
    for feature in geojson_data['features']:
        country_id = feature['properties'].get('NAME', feature['properties'].get('ADMIN'))
        
        # Determine color based on selection
        if country_id == selected_country:
            fillcolor = 'red'
            line_color = 'darkred'
            line_width = 3
        else:
            fillcolor = 'lightblue'
            line_color = 'white'
            line_width = 1
        
        # Add each country as a separate trace
        fig.add_trace(go.Choroplethmapbox(
            geojson=feature,
            locations=[0],
            z=[1],
            colorscale=[[0, fillcolor], [1, fillcolor]],
            showscale=False,
            marker_line_color=line_color,
            marker_line_width=line_width,
            hovertemplate=f"<b>{country_id}</b><extra></extra>",
            customdata=[country_id]
        ))
    
    fig.update_layout(
        margin={"r":0,"t":0,"l":0,"b":0},
        mapbox_style="carto-positron",
        clickmode='event+select'
    )
    
    return fig, selected_country

# @app.callback(
#     Output("click-info", "children"),
#     Input("graph", "clickData")
# )
# def display_click_data(clickData):
#     if clickData is None:
#         return "Click on a region to see information"
    
#     # Extract information from click event
#     point = clickData['points'][0]
    
#     # Get location and other data
#     location = point.get('location', 'Unknown')
#     color_value = point.get('z', 'No data')
#     hover_text = point.get('hovertext', 'No text')
    
#     return html.Div([
#         html.H5("Clicked Region Information:"),
#         html.P(f"Location: {location}"),
#         html.P(f"Value: {color_value}"),
#         html.P(f"Details: {hover_text}")
#     ])

app.run(debug=True)