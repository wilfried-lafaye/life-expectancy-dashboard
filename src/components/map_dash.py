import folium
import numpy as np


def create_map(df, world_gj, selected_year, selected_sex):
    """
    Génère une carte choroplèthe Folium avec tooltip au survol.
    """
    # Filtrer les données selon sélection
    subset = df[(df["TimeDim"] == selected_year) & (df["Dim1"] == selected_sex)].copy()

    # Créer un dictionnaire pour accès rapide : code pays -> valeur
    life_exp_dict = dict(zip(subset["SpatialDim"], subset["NumericValue"]))

    # Ajouter les valeurs dans le GeoJSON
    for feature in world_gj['features']:
        country_code = feature.get('id')  # Récupère l'ID du pays
        if country_code and country_code in life_exp_dict:
            feature['properties']['life_expectancy'] = round(life_exp_dict[country_code], 1)
        else:
            feature['properties']['life_expectancy'] = 'N/A'

    # Calculer l'échelle de couleurs
    values = subset["NumericValue"].dropna().values
    if len(values) == 0:
        vmin, vmax = 60, 90
    else:
        vmin, vmax = np.percentile(values, 2), np.percentile(values, 98)

    # Créer la carte
    m = folium.Map(zoom_start=2, location=[20, 0], tiles="cartodb positron")

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
    choropleth.add_to(m)

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

    return m._repr_html_()
