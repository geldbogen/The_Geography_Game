import dash_leaflet as dl
import dash_leaflet.express as dlx
from dash_extensions.enrich import DashProxy, Input, Output, State, html
from dash_extensions.javascript import arrow_function

# Generate some in-memory data, and add a simple popup with the name.
bermuda = dlx.dicts_to_geojson([dict(lat=32.299507, lon=-64.790337, popup="Bermuda")])
bahamas = dlx.geojson_to_geobuf(dlx.dicts_to_geojson([dict(lat=24.55, lon=-78, popup="Bahamas")]))
# Create example app.
app = DashProxy()
app.layout = html.Div(
    [
        dl.Map(
            center=[39, -98],
            zoom=4,
            children=[
                dl.TileLayer(),
                dl.GeoJSON(
                    url="world_map.geojson", 
                    id="my_geojson",
                    hideout=dict(selected=[]),
                    style=arrow_function("""
                        function(feature, context) {
                            const {selected} = context.hideout;
                            const isSelected = selected.includes(feature.properties.NAME || feature.properties.name);
                            return {
                                fillColor: isSelected ? 'red' : 'lightblue',
                                fillOpacity: 0.7,
                                color: 'white',
                                weight: 2
                            };
                        }
                    """),
                ),  # geojson resource (faster than in-memory)
            ],
            style={"height": "50vh"},
        ),
        html.Div(id="capital"),
        html.Div(id="selected-info", style={'margin-top': '20px', 'padding': '10px'}),
    ]
)


@app.callback(
    Output("my_geojson", "hideout"),
    Input("my_geojson", "n_clicks"),
    State("my_geojson", "clickData"),
    State("my_geojson", "hideout"),
    prevent_initial_call=True,
)
def toggle_select(_, feature, hideout):
    if not feature:
        return hideout
    
    selected = hideout["selected"]
    # Try different property names that might exist in your GeoJSON
    name = feature["properties"].get("NAME") or feature["properties"].get("name") or feature["properties"].get("ADMIN")
    
    if not name:
        return hideout
    
    if name in selected:
        selected.remove(name)
    else:
        selected.append(name)
    
    # Update hideout to trigger style change
    hideout["selected"] = selected
    
    return hideout

# Add callback to show selected countries
@app.callback(
    Output("selected-info", "children"),
    Input("my_geojson", "hideout")
)
def display_selected_countries(hideout):
    selected = hideout.get("selected", [])
    if not selected:
        return "Click on countries to select them. Selected countries will turn red."
    
    return html.Div([
        html.H5("Selected Countries:"),
        html.Ul([html.Li(country) for country in selected])
    ])



if __name__ == "__main__":
    app.run(port=7777)
