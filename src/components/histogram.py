"""
Histogram visualization module.
Displays the distribution of countries by life expectancy ranges,
with Year & Sex filters and hover showing counts by WHO region.
"""

import pandas as pd
import dash_bootstrap_components as dbc
from dash import dcc, html, Input, Output, callback

from scripts.create_who_regions import WHO_REGIONS
from src.utils.get_data import load_clean_data

# -------------------- LOAD DATA (read-only) --------------------
df = load_clean_data().copy()

# Safety
for col in ("TimeDim", "NumericValue", "SpatialDim", "Dim1"):
    if col not in df.columns:
        df[col] = pd.NA

df["TimeDim"] = pd.to_numeric(df["TimeDim"], errors="coerce")
df["NumericValue"] = pd.to_numeric(df["NumericValue"], errors="coerce")
df["SpatialDim"] = df["SpatialDim"].astype(str)

# ---- NORMALISE Dim1 (sex) into a new column Dim1_norm ----
def normalise_sex(series: pd.Series) -> pd.Series:
    s = (
        series.astype(str)
        .str.strip()
        .str.lower()
        .str.replace(r"[\s\-_]", "", regex=True)
    )
    mapping = {
        "sexbtsx": "SEX_BTSX", "btsx": "SEX_BTSX", "bothsexes": "SEX_BTSX", "bothsex": "SEX_BTSX", "both": "SEX_BTSX",
        "sexfmle": "SEX_FMLE", "fmle": "SEX_FMLE", "female": "SEX_FMLE", "femme": "SEX_FMLE", "f": "SEX_FMLE",
        "sexmle": "SEX_MLE", "mle": "SEX_MLE", "male": "SEX_MLE", "homme": "SEX_MLE", "m": "SEX_MLE",
    }
    out = s.map(mapping)
    # si déjà au bon format, on le garde
    mask_exact = series.isin(["SEX_BTSX", "SEX_FMLE", "SEX_MLE"])
    out.loc[mask_exact] = series.loc[mask_exact]
    return out

df["Dim1_norm"] = normalise_sex(df["Dim1"])

# Available years
years = sorted(df["TimeDim"].dropna().unique().tolist())

# UI labels -> codes (ce qu’on veut dans Dim1_norm)
SEX_LABEL_TO_CODE = {"Both sexes": "SEX_BTSX", "Female": "SEX_FMLE", "Male": "SEX_MLE"}

# -------------------- LAYOUT --------------------
layout = dbc.Container(
    [
        html.H2("Number of countries by life expectancy range"),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Label("Year", html_for="year-dropdown-hist", className="mb-1"),
                        dcc.Dropdown(
                            id="year-dropdown-hist",
                            options=[{"label": int(y), "value": int(y)} for y in years] if years else [],
                            value=int(years[-1]) if years else None,
                            clearable=False,
                            style={"minWidth": "200px"},
                        ),
                    ],
                    xs=12, sm=6, md=3, lg=2,
                ),
                dbc.Col(
                    [
                        dbc.Label("Sex", className="mb-1"),
                        dcc.RadioItems(
                            id="sex-radio-hist",
                            options=[{"label": k, "value": k} for k in ["Both sexes", "Female", "Male"]],
                            value="Both sexes",
                            inline=True,
                            labelStyle={"marginRight": "1rem"},
                        ),
                    ],
                    xs=12, sm=6, md="auto",
                ),
            ],
            className="g-3 mb-2",
            align="end",
        ),
        dcc.Graph(id="histogram"),
    ],
    style={"marginTop": "2rem"},
)

# -------------------- CALLBACK --------------------
@callback(
    Output("histogram", "figure"),
    [Input("year-dropdown-hist", "value"), Input("sex-radio-hist", "value")],
)
def update_histogram(selected_year, selected_sex_label):
    # 1) Filter by year
    if selected_year is None:
        d = df.copy()
    else:
        d = df[df["TimeDim"] == int(selected_year)].copy()

    # 2) Filter by sex (robuste grâce à Dim1_norm)
    sex_code = SEX_LABEL_TO_CODE.get(selected_sex_label, "SEX_BTSX")
    d = d[d["Dim1_norm"] == sex_code].copy()

    # --- Si rien après filtrage, on affiche un message explicite
    if d.empty:
        return {
            "data": [],
            "layout": {
                "title": f"No data for {selected_year} — {selected_sex_label}",
                "xaxis": {"title": "Life expectancy ranges (years)"},
                "yaxis": {"title": "Number of countries"},
                "height": 400,
            },
        }

    # 3) Bins
    bins = [40, 50, 60, 70, 80, 90]
    labels = [f"{bins[i]}–{bins[i+1]-1}" for i in range(len(bins) - 1)]
    d["age_bin"] = pd.cut(d["NumericValue"], bins=bins, labels=labels, right=False)

    # counts per bin + list of unique ISO3 per bin
    country_counts = d.groupby("age_bin", observed=True)["SpatialDim"].nunique()
    country_names = d.groupby("age_bin", observed=True)["SpatialDim"].unique()

    # 4) Détail par région OMS pour chaque barre
    region_breakdown = {}
    for age_bin, countries in country_names.items():
        region_breakdown[age_bin] = {}
        for region_key, region_info in WHO_REGIONS.items():
            cnt = sum(1 for c in countries if c in region_info["countries"])
            if cnt > 0:
                region_breakdown[age_bin][region_info["name"]] = cnt

    # 5) Hover text (totaux + détail par région)
    hover_texts = []
    for age_bin in labels:  # ordre stable
        total = int(country_counts.get(age_bin, 0))
        lines = [f"<b>{age_bin} years</b>", f"Total: {total} countries", ""]
        for region_name in sorted(region_breakdown.get(age_bin, {}).keys()):
            cnt = region_breakdown[age_bin][region_name]
            lines.append(f"{region_name}: {cnt} {'country' if cnt == 1 else 'countries'}")
        hover_texts.append("<br>".join(lines))

    # 6) Figure
    fig = {
        "data": [
            {
                "x": [str(x) for x in labels],
                "y": [int(country_counts.get(lb, 0)) for lb in labels],
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
            "height": 400,
            "margin": {"l": 50, "r": 30, "t": 30, "b": 60},
            "title": f"{selected_year} — {selected_sex_label}",
        },
    }
    return fig
