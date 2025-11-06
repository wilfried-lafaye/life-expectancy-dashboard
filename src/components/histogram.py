"""
Histogram visualization module.
Displays the distribution of countries by life expectancy ranges.
"""

import math
import pandas as pd
import plotly.io as pio
import dash_bootstrap_components as dbc
from dash import dcc, html, Input, Output, callback
from scripts.build_regional_geojson import WHO_REGIONS
from src.utils.get_data import load_clean_data

df = load_clean_data()

# Extract available years
years = sorted(df["TimeDim"].dropna().unique().tolist())

layout = dbc.Container(
    [
        html.H2("Number of countries by life expectancy range"),
        dbc.Row(
            [
                dbc.Col(
                    dcc.Dropdown(
                        id="year-dropdown-hist",
                        options=[{"label": year, "value": year} for year in years],
                        value=years[-1] if years else None,
                        clearable=False,
                        style={"width": "220px"},
                    ),
                    md="auto",
                ),
                dbc.Col(
                    dcc.Dropdown(
                        id="sex-dropdown-hist",
                        options=[
                            {"label": "Both sexes", "value": "Both"},
                            {"label": "Female", "value": "Female"},
                            {"label": "Male", "value": "Male"},
                        ],
                        value="Both",
                        clearable=False,
                        style={"width": "220px"},
                    ),
                    md="auto",
                ),
                dbc.Col(
                    dcc.Dropdown(
                        id="bin-width",
                        options=[
                            {"label": "2 years", "value": 2},
                            {"label": "5 years", "value": 5},
                            {"label": "10 years", "value": 10},
                        ],
                        value=5,
                        clearable=False,
                        style={"width": "160px"},
                    ),
                    md="auto",
                ),
            ],
            className="g-2 mb-3",
        ),
        dcc.Graph(id="histogram"),
    ],
    style={"marginTop": "2rem"},
)

# Global template (once in app startup)
pio.templates["app_light"] = pio.templates["simple_white"].update({
    "layout": {
        "font": {"family": "Inter, Segoe UI, system-ui, sans-serif", "size": 14, "color": "#222"},
        "paper_bgcolor": "white",
        "plot_bgcolor": "white",
        "colorway": ["#2563EB", "#059669", "#D97706", "#7C3AED"],
        "xaxis": {"gridcolor": "#eee"},
        "yaxis": {"gridcolor": "#eee"},
    }
})
pio.templates.default = "app_light"


@callback(
    Output("histogram", "figure"),
    Input("year-dropdown-hist", "value"),
    Input("sex-dropdown-hist", "value"),
    Input("bin-width", "value"),
)
def update_histogram(selected_year, selected_sex, step):
    """
    Updates the histogram based on the selected year, sex and bin width.
    """
    # --- Filter by year ---
    d = df.copy() if selected_year is None else df[df["TimeDim"] == selected_year].copy()

    # --- Filter by sex ---
    if selected_sex:
        d = d[d["Dim1"] == selected_sex].copy()

    # --- Build dynamic bins from data range ---
    vals = pd.to_numeric(d["NumericValue"], errors="coerce").dropna()
    if vals.empty:
        return _empty_fig("No data for this selection.")

    vmin, vmax = float(vals.min()), float(vals.max())
    low = int(math.floor(vmin / step) * step)
    high = int(math.ceil(vmax / step) * step)
    if high <= low:
        high = low + step

    bins = list(range(low, high + step, step))
    labels = [f"{bins[i]}–{bins[i+1]-1}" for i in range(len(bins) - 1)]

    d["age_bin"] = pd.cut(
        vals,
        bins=bins,
        labels=labels,
        right=False,
        include_lowest=True,
    )

    # --- Counts per bin ---
    country_counts = d.groupby("age_bin", observed=True)["SpatialDim"].nunique()
    country_names = d.groupby("age_bin", observed=True)["SpatialDim"].unique()

    # Per-region details (for hover)
    region_counts_by_age = build_region_counts(country_names)
    hover_texts = create_hover_texts(country_counts, region_counts_by_age)

    # --- Figure ---
    fig = {
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
            "xaxis": {
                "title": "Life expectancy ranges (years)",
                "categoryorder": "array",
                "categoryarray": labels,
            },
            "yaxis": {"title": "Number of countries"},
            "height": 420,
            "margin": {"l": 50, "r": 30, "t": 30, "b": 60},
        },
    }
    return fig


def build_region_counts(country_names):
    """Builds a dictionary of region counts per age bin."""
    region_counts = {}
    for age_bin, countries in country_names.items():
        region_counts[age_bin] = {}
        for region_info in WHO_REGIONS.values():
            count = sum(1 for country in countries if country in region_info["countries"])
            if count > 0:
                region_counts[age_bin][region_info["name"]] = count
    return region_counts


def create_hover_texts(country_counts, region_counts_by_age):
    """Creates hover text for each bar with region breakdown."""
    hover_texts = []
    for age_bin in country_counts.index:
        lines = [f"{age_bin} years", f"Total: {country_counts[age_bin]} countries", ""]
        region_data = region_counts_by_age.get(age_bin, {})
        for region_name in sorted(region_data.keys()):
            count = region_data[region_name]
            plural = "country" if count == 1 else "countries"
            lines.append(f"{region_name}: {count} {plural}")
        hover_texts.append("<br>".join(lines))
    return hover_texts


def _empty_fig(msg: str):
    return {
        "data": [],
        "layout": {
            "title": msg,
            "xaxis": {"title": "Life expectancy ranges (years)"},
            "yaxis": {"title": "Number of countries"},
            "height": 420,
        },
    }
