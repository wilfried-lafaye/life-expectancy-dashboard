"""
Histogram visualization module.
Displays the distribution of countries by life expectancy ranges.
"""

import pandas as pd
import dash_bootstrap_components as dbc
from dash import dcc, html, Input, Output, callback

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
        filtered_df = df.copy()  # ✅ Fix 1: Added .copy()
    else:
        filtered_df = df[df["TimeDim"] == selected_year].copy()  # ✅ Fix 1: Added .copy()

    bins = [40, 50, 60, 70, 80, 90]
    labels = [f"{bins[i]}–{bins[i+1]-1}" for i in range(len(bins)-1)]
    filtered_df["age_bin"] = pd.cut(
        filtered_df["NumericValue"],
        bins=bins,
        labels=labels,
        right=False
    )
    # ✅ Fix 2: Added observed=True
    country_counts = filtered_df.groupby("age_bin", observed=True)["SpatialDim"].nunique()

    figure = {
        "data": [
            {
                "x": country_counts.index.astype(str),
                "y": country_counts.values,
                "type": "bar",
                "marker": {"color": "#0078D4"},
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
