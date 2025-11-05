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

    # Construire le dictionnaire avec le nombre de pays par région pour chaque age_bin
    A = {}
    for age_bin, countries in country_names.items():
        A[age_bin] = {}
        for region_key, region_info in WHO_REGIONS.items():
            count = 0
            for country in countries:
                if country in region_info['countries']:
                    count += 1
            if count > 0:
                A[age_bin][region_info['name']] = count

    # Créer les textes de hover à partir du dictionnaire A
    hover_texts = []
    for age_bin in country_counts.index:
        # Construire le texte pour cette barre
        hover_lines = [
            f"<b>{age_bin} years</b>",
            f"Total: {country_counts[age_bin]} countries",
            ""
        ]
        
        # Ajouter les détails par région (triés alphabétiquement)
        region_data = A.get(age_bin, {})
        for region_name in sorted(region_data.keys()):
            count = region_data[region_name]
            hover_lines.append(f"{region_name}: {count} {'country' if count == 1 else 'countries'}")
        
        hover_texts.append("<br>".join(hover_lines))

    figure = {
        "data": [
            {
                "x": country_counts.index.astype(str),
                "y": country_counts.values,
                "type": "bar",
                "marker": {"color": "#0078D4"},
                "hovertext": hover_texts,
                "hoverinfo": "text",
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
