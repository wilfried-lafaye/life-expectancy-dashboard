"""
Module de création de carte choroplèthe.
Génère une carte Folium interactive avec tooltip au survol.
"""

import folium


def create_map(df, world_gj, selected_year, selected_sex):
    """
    Génère une carte choroplèthe Folium avec tooltip au survol.

    Args:
        df (pd.DataFrame): DataFrame contenant les données d'espérance de vie
        world_gj (dict): GeoJSON des pays du monde
        selected_year (int): Année sélectionnée
        selected_sex (str): Sexe sélectionné ('Male', 'Female', 'Both')

    Returns:
        str: HTML de la carte Folium
    """
    # Filtrer les données selon sélection
    subset = df[
        (df["TimeDim"] == selected_year) & (df["Dim1"] == selected_sex)
    ].copy()

    # Créer un dictionnaire pour accès rapide : code pays -> valeur
    life_exp_dict = dict(zip(subset["SpatialDim"], subset["NumericValue"]))

    # Ajouter les valeurs dans le GeoJSON
    for feature in world_gj['features']:
        country_code = feature.get('id')  # Récupère l'ID du pays
        if country_code and country_code in life_exp_dict:
            feature['properties']['life_expectancy'] = round(
                life_exp_dict[country_code], 1
            )
        else:
            feature['properties']['life_expectancy'] = 'N/A'

    # Créer la carte
    folium_map = folium.Map(
        zoom_start=2,
        location=[20, 0],
        tiles="cartodb positron"
    )

    # Ajouter la couche choroplèthe
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

    # Ajouter le tooltip sur la couche GeoJson interne du Choropleth
    choropleth.geojson.add_child(
        folium.features.GeoJsonTooltip(
            fields=['name', 'life_expectancy'],
            aliases=['Pays:', 'Espérance de vie:'],
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

    # Retourner le HTML de la carte
    # pylint: disable=protected-access
    return folium_map._repr_html_()
