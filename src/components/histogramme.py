"""
Histogram visualization module.
Displays the distribution of countries by life expectancy ranges.
"""

import pandas as pd
import dash_bootstrap_components as dbc
from dash import dcc, html, Input, Output, callback

from src.utils.create_who_regions import WHO_REGIONS
from src.utils.get_data import load_clean_data

df = load_clean_data()

# Extract available years
years = sorted(df["TimeDim"].dropna().unique().tolist())

layout = dbc.Container([
    html.H2("Number of countries by life expectancy range"),
    dcc.Dropdown(
        id="year-dropdown-hist",
        options=[{"label": year, "value": year} for year in years],
        value=years[-1] if years else None,
        clearable=False,
        style={"width": "200px", "marginBottom": "1rem"}
    ),
    dcc.Graph(id="histogram"),
], style={"marginTop": "2rem"})


@callback(
    Output("histogram", "figure"),
    Input("year-dropdown-hist", "value")
)
def update_histogram(selected_year):
    """
    Updates the histogram based on the selected year.

    Args:
        selected_year: The year selected by the user

    Returns:
        dict: Plotly figure of the histogram
    """
    if selected_year is None:
        filtered_df = df.copy()
    else:
        filtered_df = df[df["TimeDim"] == selected_year].copy()

    bins = [40, 50, 60, 70, 80, 90]
    labels = [f"{bins[i]}–{bins[i+1]-1}" for i in range(len(bins)-1)]
    filtered_df["age_bin"] = pd.cut(
        filtered_df["NumericValue"],
        bins=bins,
        labels=labels,
        right=False
    )

    country_counts = filtered_df.groupby("age_bin", observed=True)["SpatialDim"].nunique()
    country_names = filtered_df.groupby("age_bin", observed=True)["SpatialDim"].unique()

    # Créer un mapping inverse pays -> région WHO
    country_to_region = {}
    for region, countries in WHO_REGIONS.items():
        for country in countries:
            country_to_region[country] = region

    # Créer le texte de survol pour chaque barre
    hover_texts = []
    for age_bin in country_counts.index:
        countries = country_names[age_bin]
        
        # Grouper par région WHO
        region_counts = {}
        for country in countries:
            region = country_to_region.get(country, "Unknown")
            region_counts[region] = region_counts.get(region, 0) + 1
        
        # Construire le texte de survol
        hover_lines = [f"<b>{age_bin} years</b><br>Total: {country_counts[age_bin]} countries<br>"]
        for region, count in sorted(region_counts.items()):
            hover_lines.append(f"{region}: {count} countries")
        
        hover_texts.append("<br>".join(hover_lines))

    figure = {
        "data": [
            {
                "x": country_counts.index.astype(str),
                "y": country_counts.values,
                "type": "bar",
                "marker": {"color": "#0078D4"},
                "text": hover_texts,
                "hovertemplate": "%{text}<extra></extra>",
            }
        ],
        "layout": {
            "xaxis": {"title": "Life expectancy ranges (years)"},
            "yaxis": {"title": "Number of countries"},
            "height": 400,
            "margin": {"l": 50, "r": 30, "t": 30, "b": 60}
        },
    }
    return figure
