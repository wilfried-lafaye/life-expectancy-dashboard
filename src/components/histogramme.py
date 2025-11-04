# src/components/histogramme.py  (English version)

import dash_bootstrap_components as dbc
from dash import dcc, html, Input, Output, callback
import pandas as pd
import numpy as np

from src.utils.get_data import load_clean_data

# -------------------- LOAD DATA (read-only) --------------------
df = load_clean_data()

# Minimal columns (safety if something is missing)
for col in ("TimeDim", "NumericValue", "SpatialDim"):
    if col not in df.columns:
        df[col] = pd.NA

# Safe conversions (do not mutate original elsewhere)
df["TimeDim"] = pd.to_numeric(df["TimeDim"], errors="coerce")
df["NumericValue"] = pd.to_numeric(df["NumericValue"], errors="coerce")
df["SpatialDim"] = df["SpatialDim"].astype(str)

# Available years
years = sorted(df["TimeDim"].dropna().unique().tolist())

# -------------------- LAYOUT --------------------
layout = dbc.Container(
    [
        html.H2("Countries by life-expectancy range and region"),
        dcc.Dropdown(
            id="year-dropdown-hist",
            options=[{"label": int(y), "value": int(y)} for y in years] if years else [],
            value=int(years[-1]) if years else None,
            clearable=False,
            style={"width": "220px", "marginBottom": "1rem"},
        ),
        dcc.Graph(id="histogram"),
    ],
    style={"marginTop": "2rem"},
)

# -------------------- CALLBACK --------------------
@callback(
    Output("histogram", "figure"),
    Input("year-dropdown-hist", "value")
)
def update_histogram(selected_year):
    # 1) Subset (always work on a copy)
    if selected_year is None or pd.isna(selected_year):
        d = df.copy()
    else:
        d = df[df["TimeDim"] == int(selected_year)].copy()

    # 2) Region normalization (and later we EXCLUDE unknowns)
    if "ParentLocation" not in d.columns:
        d["ParentLocation"] = pd.NA
    else:
        d["ParentLocation"] = d["ParentLocation"].astype(str)
        d["ParentLocation"] = d["ParentLocation"].replace(
            {"": pd.NA, "nan": pd.NA, "NaN": pd.NA, "None": pd.NA}
        )

        mapping = {
            "africa": "Africa",
            "americas": "Americas",
            "eastern mediterranean": "Eastern Mediterranean",
            "europe": "Europe",
            "south-east asia": "South-East Asia",
            "south east asia": "South-East Asia",
            "western pacific": "Western Pacific",
        }
        # Normalize labels; fallback to Title Case when not in mapping
        norm = d["ParentLocation"].dropna().astype(str).str.strip()
        mapped = norm.str.lower().map(mapping)
        d.loc[norm.index, "ParentLocation"] = mapped.fillna(norm.str.title())

    # EXCLUDE Unknown / missing regions
    d["ParentLocation"] = d["ParentLocation"].replace({"Unknown": pd.NA})
    d = d.dropna(subset=["ParentLocation"])

    # 3) Life-expectancy bins
    bins = [40, 50, 60, 70, 80, 90]
    labels = [f"{bins[i]}–{bins[i+1]-1}" for i in range(len(bins) - 1)]
    d["NumericValue"] = pd.to_numeric(d["NumericValue"], errors="coerce")
    age_bin = pd.cut(
        d["NumericValue"], bins=bins, labels=labels, right=False, include_lowest=True
    )

    # 4) Count unique countries per (range, region)
    g = (
        pd.DataFrame({
            "age_bin": age_bin,
            "region": d["ParentLocation"],
            "iso3": d["SpatialDim"].astype(str),
        })
        .dropna(subset=["age_bin", "region"])
        .groupby(["age_bin", "region"])["iso3"]
        .nunique()
        .rename("nb_countries")
        .reset_index()
    )

    # If nothing remains (after excluding unknowns)
    if g.empty:
        return {
            "data": [],
            "layout": {
                "title": "No data for this filter (unknown regions excluded)",
                "xaxis": {"title": "Life expectancy ranges (years)"},
                "yaxis": {"title": "Number of countries"},
                "height": 420,
            },
        }

    # 5) Totals per range (bar height) + hover text with regional breakdown
    totals = (
        g.groupby("age_bin")["nb_countries"].sum()
         .reindex(labels, fill_value=0)
    )

    hover_texts = []
    for ab in labels:
        block = g[g["age_bin"] == ab].copy()
        if block.empty or totals.loc[ab] == 0:
            hover_texts.append("No details available")
            continue

        block = block.sort_values("nb_countries", ascending=False)
        tot = totals.loc[ab]
        lines = [
            f"{row['region']}: {int(row['nb_countries'])} countries ({row['nb_countries'] / tot * 100:.1f}%)"
            for _, row in block.iterrows()
            if row["nb_countries"] > 0
        ]
        hover_texts.append("<br>".join(lines))

    # Plotly prefers 2D customdata for robust hover
    customdata = [[txt] for txt in hover_texts]

    # 6) Single trace (one color); hover shows regional details
    trace = {
        "type": "bar",
        "name": "Total",
        "x": list(totals.index.astype(str)),
        "y": totals.values.tolist(),
        "marker": {"color": "#0078D4"},
        "customdata": customdata,
        "hoverlabel": {"align": "left"},
        "hovertemplate": (
            "<b>%{x}</b><br>"
            "Total: %{y} countries<br>"
            "%{customdata[0]}"
            "<extra></extra>"
        ),
    }

    fig = {
        "data": [trace],
        "layout": {
            "barmode": "group",
            "xaxis": {
                "title": "Life expectancy ranges (years)",
                "categoryorder": "array",
                "categoryarray": labels,
            },
            "yaxis": {"title": "Number of countries"},
            "height": 420,
            "margin": {"l": 50, "r": 30, "t": 60, "b": 60},
            "legend": {"title": {"text": "Region"}, "traceorder": "normal"},
            "title": (
                f"Countries by life-expectancy range — {int(selected_year)}"
                if selected_year is not None and not pd.isna(selected_year)
                else "Countries by life-expectancy range — all years"
            ),
        },
    }
    return fig
