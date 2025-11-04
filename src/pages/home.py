"""
Dashboard home page module.

Contains the choropleth map layout and associated callbacks.
"""

from dash import dcc, html, Output, Input
import dash_bootstrap_components as dbc

from src.utils.get_data import load_clean_data, load_world_geojson, load_who_regions_geojson
from src.components.map import create_map

df = load_clean_data()
world_gj = load_world_geojson()
regions_gj = load_who_regions_geojson()

years = sorted(df["TimeDim"].dropna().unique().tolist())
sex_codes_avail_raw = ['Female', 'Both', 'Male']

page_layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H1("Life expectancy at birth — world choropleth"),
            html.Label("Year"),
            dcc.Dropdown(
                id="year-dropdown",
                options=[{"label": y, "value": y} for y in years],
                value=years[-1]
            ),
            html.Br(),
            html.Label("Sex"),
            dcc.RadioItems(
                id="sex-radio",
                options=[
                    {"label": s, "value": s} for s in sex_codes_avail_raw
                ],
                value="Female"
            ),
            html.Br(),
            html.Label("Display by"),
            dcc.RadioItems(
                id="spatial-type-radio",
                options=[
                    {"label": "Country", "value": "COUNTRY"},
                    {"label": "Region", "value": "REGION"}
                ],
                value="COUNTRY"
            ),
        ], width=3, style={
            "padding": "20px",
            "backgroundColor": "#f8f9fa",
            "borderRadius": "8px"
        }),
        dbc.Col([
            html.Iframe(
                id="map-iframe",
                style={
                    "border": "none",
                    "width": "100%",
                    "height": "600px"
                }
            )
        ], width=9)
    ])
], fluid=True)


def register_callbacks(app):
    """
    Registers callbacks for the map page.
    
    Args:
        app: The Dash application instance
    """
    @app.callback(
        Output("map-iframe", "srcDoc"),
        [
            Input("year-dropdown", "value"),
            Input("sex-radio", "value"),
            Input("spatial-type-radio", "value")
        ]
    )
    def update_map(year_selected, sex_selected, spatial_type_selected):
        """
        Updates the map based on the selected year, sex, and spatial type.
        
        Args:
            year_selected: The selected year
            sex_selected: The selected sex
            spatial_type_selected: 'COUNTRY' or 'REGION'
        
        Returns:
            str: The Folium map HTML
        """
        # Choose the appropriate GeoJSON
        geojson = world_gj if spatial_type_selected == 'COUNTRY' else regions_gj
        
        return create_map(df, geojson, year_selected, sex_selected, spatial_type_selected)
