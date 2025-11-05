"""
Histogram visualization module.
Displays the distribution of countries by life expectancy ranges.
"""

import pandas as pd
import dash_bootstrap_components as dbc
from dash import dcc, html, Input, Output, callback
from scripts.create_who_regions import WHO_REGIONS
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
    dcc.Dropdown(
        id="sex-dropdown-hist",
        options=[
            {"label": "Both sexes", "value": "Both"},
            {"label": "Male", "value": "Male"},
            {"label": "Female", "value": "Female"}
        ],
        value="Both",
        clearable=False,
        style={"width": "200px", "marginBottom": "1rem"}
    ),
    dcc.Graph(id="histogram"),
], style={"marginTop": "2rem"})

@callback(
    Output("histogram", "figure"),
    Input("year-dropdown-hist", "value"),
    Input("sex-dropdown-hist", "value")
)
def update_histogram(selected_year, selected_sex):
    """
    Updates the histogram based on the selected year and sex.

    Args:
        selected_year: The year selected by the user
        selected_sex: The sex filter selected by the user

    Returns:
        dict: Plotly figure of the histogram
    """
    # Filter by year
    if selected_year is None:
        filtered_df = df.copy()
    else:
        filtered_df = df[df["TimeDim"] == selected_year].copy()

    # Filter by sex
    if selected_sex:
        filtered_df = filtered_df[filtered_df["Dim1"] == selected_sex].copy()

    # Define bins and labels
    bins = [40, 50, 60, 70, 80, 90]
    labels = [f"{bins[i]}–{bins[i+1]-1}" for i in range(len(bins)-1)]

    # Create age bins
    filtered_df["age_bin"] = pd.cut(
        filtered_df["NumericValue"],
        bins=bins,
        labels=labels,
        right=False
    )

    # Count countries per bin
    country_counts = (
        filtered_df.groupby("age_bin", observed=True)["SpatialDim"].nunique()
    )

    # Get country names per bin
    country_names = (
        filtered_df.groupby("age_bin", observed=True)["SpatialDim"].unique()
    )

    # Build region counts dictionary
    region_counts_by_age = build_region_counts(country_names)

    # Create hover texts
    hover_texts = create_hover_texts(country_counts, region_counts_by_age)

    # Create figure
    figure = {
        "data": [{
            "x": country_counts.index.astype(str),
            "y": country_counts.values,
            "type": "bar",
            "marker": {"color": "#0078D4"},
            "hovertext": hover_texts,
            "hoverinfo": "text",
        }],
        "layout": {
            "xaxis": {"title": "Life expectancy ranges (years)"},
            "yaxis": {"title": "Number of countries"},
            "height": 400,
            "margin": {"l": 50, "r": 30, "t": 30, "b": 60}
        },
    }

    return figure

def build_region_counts(country_names):
    """
    Builds a dictionary of region counts per age bin.

    Args:
        country_names: Dictionary of countries grouped by age bin

    Returns:
        dict: Region counts by age bin
    """
    region_counts = {}
    for age_bin, countries in country_names.items():
        region_counts[age_bin] = {}
        for region_info in WHO_REGIONS.values():
            count = sum(1 for country in countries
                       if country in region_info['countries'])
            if count > 0:
                region_counts[age_bin][region_info['name']] = count
    return region_counts

def create_hover_texts(country_counts, region_counts_by_age):
    """
    Creates hover text for each bar in the histogram.

    Args:
        country_counts: Series of country counts per age bin
        region_counts_by_age: Dictionary of region counts per age bin

    Returns:
        list: Hover texts for each bar
    """
    hover_texts = []
    for age_bin in country_counts.index:
        hover_lines = [
            f"{age_bin} years",
            f"Total: {country_counts[age_bin]} countries",
            ""
        ]

        region_data = region_counts_by_age.get(age_bin, {})
        for region_name in sorted(region_data.keys()):
            count = region_data[region_name]
            plural = 'country' if count == 1 else 'countries'
            hover_lines.append(f"{region_name}: {count} {plural}")

        hover_texts.append("<br>".join(hover_lines))

    return hover_texts
