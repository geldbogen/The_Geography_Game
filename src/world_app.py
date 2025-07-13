import dash
from dash import dcc, html, Input, Output, callback
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

# Initialize the Dash app
app = dash.Dash(__name__, 
                external_stylesheets=[dbc.themes.BOOTSTRAP],
                meta_tags=[{'name': 'viewport', 'content': 'width=device-width, initial-scale=1'}])

app.title = "Interactive World Map"

# Sample data for countries (you can replace this with your own data)
sample_data = {
    'country': ['United States', 'Canada', 'Mexico', 'Brazil', 'Argentina', 'United Kingdom', 
                'France', 'Germany', 'Spain', 'Italy', 'Russia', 'China', 'Japan', 'India',
                'Australia', 'South Africa', 'Egypt', 'Nigeria', 'Kenya', 'Morocco'],
    'iso_alpha': ['USA', 'CAN', 'MEX', 'BRA', 'ARG', 'GBR', 'FRA', 'DEU', 'ESP', 'ITA', 
                  'RUS', 'CHN', 'JPN', 'IND', 'AUS', 'ZAF', 'EGY', 'NGA', 'KEN', 'MAR'],
    'population': [331900000, 38000000, 128900000, 212600000, 45200000, 67900000,
                   67400000, 83200000, 47400000, 60400000, 145900000, 1439300000,
                   125800000, 1380000000, 25700000, 59300000, 102300000, 206100000,
                   53800000, 36900000],
    'gdp_per_capita': [65280, 46260, 9680, 8710, 10040, 42330, 40490, 46260, 27060,
                       31400, 11290, 10500, 39290, 1900, 51810, 6010, 3020, 2230,
                       1760, 3120],
    'continent': ['North America', 'North America', 'North America', 'South America', 
                  'South America', 'Europe', 'Europe', 'Europe', 'Europe', 'Europe',
                  'Asia', 'Asia', 'Asia', 'Asia', 'Oceania', 'Africa', 'Africa', 
                  'Africa', 'Africa', 'Africa']
}

df = pd.DataFrame(sample_data)

# Create the layout
app.layout = dbc.Container([
    # Header
    dbc.Row([
        dbc.Col([
            html.H1("Interactive World Map", className="text-center mb-4 text-primary"),
            html.P("Explore countries around the world with interactive data visualization", 
                   className="text-center text-muted mb-4")
        ])
    ]),
    
    # Controls
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Map Controls"),
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col([
                            dbc.Label("Color by:"),
                            dcc.Dropdown(
                                id='color-dropdown',
                                options=[
                                    {'label': 'Population', 'value': 'population'},
                                    {'label': 'GDP per Capita', 'value': 'gdp_per_capita'},
                                    {'label': 'Continent', 'value': 'continent'}
                                ],
                                value='population',
                                clearable=False
                            )
                        ], width=6),
                        dbc.Col([
                            dbc.Label("Map Projection:"),
                            dcc.Dropdown(
                                id='projection-dropdown',
                                options=[
                                    {'label': 'Natural Earth', 'value': 'natural earth'},
                                    {'label': 'Mercator', 'value': 'mercator'},
                                    {'label': 'Orthographic', 'value': 'orthographic'},
                                    {'label': 'Equirectangular', 'value': 'equirectangular'},
                                    {'label': 'Robinson', 'value': 'robinson'}
                                ],
                                value='natural earth',
                                clearable=False
                            )
                        ], width=6)
                    ])
                ])
            ])
        ], width=12)
    ], className="mb-4"),
    
    # Map
    dbc.Row([
        dbc.Col([
            dcc.Graph(
                id='world-map',
                style={'height': '70vh'},
                config={
                    'displayModeBar': True,
                    'displaylogo': False,
                    'modeBarButtonsToRemove': ['pan2d', 'lasso2d', 'select2d']
                }
            )
        ], width=12)
    ]),
    
    # Country Information Panel
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Country Information"),
                dbc.CardBody([
                    html.Div(id="country-info", children=[
                        html.P("Click on a country to see detailed information", 
                               className="text-muted text-center")
                    ])
                ])
            ])
        ], width=12)
    ], className="mt-4"),
    
    # Footer
    dbc.Row([
        dbc.Col([
            html.Hr(),
            html.P("Created with Dash and Plotly", 
                   className="text-center text-muted small")
        ])
    ])
    
], fluid=True, className="p-4")

# Callback to update the world map
@callback(
    Output('world-map', 'figure'),
    [Input('color-dropdown', 'value'),
     Input('projection-dropdown', 'value')]
)
def update_map(color_by, projection):
    # Create the choropleth map
    if color_by == 'continent':
        fig = px.choropleth(
            df, 
            locations="iso_alpha",
            color="continent",
            hover_name="country",
            hover_data={
                'population': ':,',
                'gdp_per_capita': ':,',
                'continent': True,
                'iso_alpha': False
            },
            color_discrete_map={
                'North America': '#1f77b4',
                'South America': '#ff7f0e', 
                'Europe': '#2ca02c',
                'Asia': '#d62728',
                'Africa': '#9467bd',
                'Oceania': '#8c564b'
            },
            title=f"World Map - Colored by {color_by.replace('_', ' ').title()}"
        )
    else:
        fig = px.choropleth(
            df, 
            locations="iso_alpha",
            color=color_by,
            hover_name="country",
            hover_data={
                'population': ':,',
                'gdp_per_capita': ':,',
                'continent': True,
                'iso_alpha': False
            },
            color_continuous_scale="Viridis",
            title=f"World Map - Colored by {color_by.replace('_', ' ').title()}"
        )
    
    # Update layout
    fig.update_layout(
        geo=dict(
            showframe=False,
            showcoastlines=True,
            projection_type=projection,
            bgcolor='rgba(0,0,0,0)'
        ),
        title={
            'text': f"World Map - Colored by {color_by.replace('_', ' ').title()}",
            'x': 0.5,
            'xanchor': 'center',
            'font': {'size': 20}
        },
        font=dict(family="Arial, sans-serif"),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=0, r=0, t=50, b=0),
        height=600
    )
    
    return fig

# Callback to update country information when clicked
@callback(
    Output('country-info', 'children'),
    Input('world-map', 'clickData')
)
def display_country_info(clickData):
    if clickData is None:
        return html.P("Click on a country to see detailed information", 
                      className="text-muted text-center")
    
    # Get the clicked country
    country_iso = clickData['points'][0]['location']
    country_data = df[df['iso_alpha'] == country_iso].iloc[0]
    
    # Create information cards
    info_cards = dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4(country_data['country'], className="card-title text-primary"),
                    html.P(f"Continent: {country_data['continent']}", className="card-text"),
                ])
            ])
        ], width=4),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H5("Population", className="card-title"),
                    html.H3(f"{country_data['population']:,}", className="text-info"),
                ])
            ])
        ], width=4),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H5("GDP per Capita", className="card-title"),
                    html.H3(f"${country_data['gdp_per_capita']:,}", className="text-success"),
                ])
            ])
        ], width=4),
    ])
    
    return info_cards

def run_world_app():
    """Function to run the world map app"""
    app.run(debug=True, port=8051)

if __name__ == '__main__':
    run_world_app()
