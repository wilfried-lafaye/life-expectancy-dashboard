"""
Choropleth map creation module.
Generates an interactive Folium map with hover tooltip.
"""

import folium

def create_map(df, world_gj, selected_year, selected_sex):
    """
    Generates a Folium choropleth map with hover tooltip.

    Args:
        df (pd.DataFrame): DataFrame containing life expectancy data
        world_gj (dict): World countries GeoJSON
        selected_year (int): Selected year
        selected_sex (str): Selected sex ('Male', 'Female', 'Both')

    Returns:
        str: Folium map HTML
    """
    # Filter data according to selection
    subset = df[
        (df["TimeDim"] == selected_year) & (df["Dim1"] == selected_sex)
    ].copy()

    # Create a dictionary for fast access: country code -> value
    life_exp_dict = dict(zip(subset["SpatialDim"], subset["NumericValue"]))

    # Add values to the GeoJSON
    for feature in world_gj['features']:
        country_code = feature.get('id')  # Get country ID
        if country_code and country_code in life_exp_dict:
            feature['properties']['life_expectancy'] = round(
                life_exp_dict[country_code], 1
            )
        else:
            feature['properties']['life_expectancy'] = 'N/A'

    # Create the map
    folium_map = folium.Map(
        zoom_start=2,
        location=[20, 0],
        tiles="cartodb positron"
    )

    # Add the choropleth layer
    choropleth = folium.Choropleth(
        geo_data=world_gj,
        name="Choropleth",
        data=subset,
        columns=["SpatialDim", "NumericValue"],
        key_on="feature.id",
        fill_color="Greens",
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name="Life expectancy at birth",
        nan_fill_color="lightgrey",
        bins=10,
        reset=True,
        smooth_factor=0,
    )
    choropleth.add_to(folium_map)

    # Add tooltip to the internal GeoJson layer of the Choropleth
    choropleth.geojson.add_child(
        folium.features.GeoJsonTooltip(
            fields=['name', 'life_expectancy'],
            aliases=['Country:', 'Life expectancy:'],
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
