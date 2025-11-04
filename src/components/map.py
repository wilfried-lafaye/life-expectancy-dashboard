"""
Choropleth map creation module.

Generates an interactive Folium map with hover tooltip.
"""

import folium


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
    # Filter data according to selection
    subset = df[
        (df["TimeDim"] == selected_year) & 
        (df["Dim1"] == selected_sex) &
        (df["SpatialDimType"] == spatial_type)
    ].copy()
    
    # Create a dictionary for fast access: code -> value
    life_exp_dict = dict(zip(subset["SpatialDim"], subset["NumericValue"]))
    
    # Add values to the GeoJSON
    for feature in geojson['features']:
        feature_id = feature.get('id')
        if feature_id and feature_id in life_exp_dict:
            feature['properties']['life_expectancy'] = round(
                life_exp_dict[feature_id], 1
            )
        else:
            feature['properties']['life_expectancy'] = 'N/A'
    
    # Create the map
    folium_map = folium.Map(
        zoom_start=2,
        location=[20, 0],
        tiles="cartodb positron"
    )
    
    # Label for legend
    legend_label = ("Life expectancy at birth (by country)" 
                   if spatial_type == 'COUNTRY' 
                   else "Life expectancy at birth (by region)")
    
    # Add the choropleth layer
    choropleth = folium.Choropleth(
        geo_data=geojson,
        name="Choropleth",
        data=subset,
        columns=["SpatialDim", "NumericValue"],
        key_on="feature.id",
        fill_color="Greens",
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name=legend_label,
        nan_fill_color="lightgrey",
        bins=10,
        reset=True,
        smooth_factor=0,
    )
    choropleth.add_to(folium_map)
    
    # Add tooltip
    tooltip_label = 'Country:' if spatial_type == 'COUNTRY' else 'Region:'
    choropleth.geojson.add_child(
        folium.features.GeoJsonTooltip(
            fields=['name', 'life_expectancy'],
            aliases=[tooltip_label, 'Life expectancy:'],
            localize=True,
            sticky=False,
            labels=True,
            style="""
                background-color: white;
                border: 2px solid #333;
                border-radius: 5px;
                padding: 8px;
                font-family: Arial, sans-serif;
                font-size: 13px;
            """,
        )
    )
    
    # Return the map HTML
    # pylint: disable=protected-access
    return folium_map._repr_html_()
