"""
Map page module - Choropleth map with controls and callbacks.
"""
from dash import dcc, html, Output, Input, callback
import dash_bootstrap_components as dbc
import folium
from src.utils.get_data import load_clean_data, load_world_geojson, load_who_regions_geojson

# Load data
df = load_clean_data()
world_gj = load_world_geojson()
regions_gj = load_who_regions_geojson()

years = sorted(df["TimeDim"].dropna().unique().tolist())
sex_codes_avail_raw = ['Female', 'Both', 'Male']

# Page layout
layout = dbc.Container([
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
                options=[{"label": s, "value": s} for s in sex_codes_avail_raw],
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
            )
        ], md=3),
        
        dbc.Col([
            html.Iframe(
                id="map-iframe",
                style={"width": "100%", "height": "600px", "border": "1px solid #ccc"}
            )
        ], md=9)
    ])
], fluid=True, style={"marginTop": "2rem"})


def create_map(df, geojson, selected_year, selected_sex, spatial_type='COUNTRY'):
    """
    Generates a Folium choropleth map with hover tooltip.
    
    Args:
        df (pd.DataFrame): DataFrame containing life expectancy data
        geojson (dict): GeoJSON (countries or regions)
        selected_year (int): Selected year
        selected_sex (str): Selected sex ('Male', 'Female', 'Both')
        spatial_type (str): 'COUNTRY' or 'REGION'
    
    Returns:
        str: Folium map HTML
    """
    # Filter data
    subset = df[
        (df["TimeDim"] == selected_year) &
        (df["Dim1"] == selected_sex) &
        (df["SpatialDimType"] == spatial_type)
    ].copy()
    
    life_exp_dict = dict(zip(subset["SpatialDim"], subset["NumericValue"]))
    
    # Add values to GeoJSON
    for feature in geojson['features']:
        feature_id = feature.get('id')
        if feature_id and feature_id in life_exp_dict:
            feature['properties']['life_expectancy'] = life_exp_dict[feature_id]
        else:
            feature['properties']['life_expectancy'] = None
    
    # Create map
    m = folium.Map(location=[20, 0], zoom_start=2, tiles="cartodb positron")
    
    folium.Choropleth(
        geo_data=geojson,
        data=subset,
        columns=["SpatialDim", "NumericValue"],
        key_on="feature.id",
        fill_color="YlOrRd",
        fill_opacity=0.7,
        line_opacity=0.3,
        legend_name=f"Life Expectancy at Birth ({selected_year}, {selected_sex})",
        nan_fill_color="lightgray"
    ).add_to(m)
    
    # Add tooltip
    folium.GeoJson(
        geojson,
        style_function=lambda x: {'fillColor': 'transparent', 'color': 'transparent'},
        tooltip=folium.GeoJsonTooltip(
            fields=['name', 'life_expectancy'],
            aliases=['Name:', 'Life Expectancy:'],
            localize=True
        )
    ).add_to(m)
    
    return m._repr_html_()


@callback(
    Output("map-iframe", "srcDoc"),
    Input("year-dropdown", "value"),
    Input("sex-radio", "value"),
    Input("spatial-type-radio", "value")
)
def update_map(selected_year, selected_sex, spatial_type):
    """Updates the map based on user selection."""
    geojson = world_gj if spatial_type == "COUNTRY" else regions_gj
    return create_map(df, geojson, selected_year, selected_sex, spatial_type)
