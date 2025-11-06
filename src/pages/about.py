"""
About page — project overview, KPIs, resources, and credits.
"""

from dash import html
import dash_bootstrap_components as dbc
import pandas as pd

from src.utils.get_data import load_clean_data

# ---------- Load data & quick stats ----------
_df = load_clean_data()

# Years
_years = _df["TimeDim"].dropna().astype(int)
year_min = int(_years.min()) if not _years.empty else None
year_max = int(_years.max()) if not _years.empty else None

# Countries (only COUNTRY level)
try:
    n_countries = (
        _df[_df["SpatialDimType"] == "COUNTRY"]["SpatialDim"].nunique()
    )
except KeyError:
    n_countries = _df["SpatialDim"].nunique()

# Sexes (as-is from the cleaned CSV)
sexes = (
    sorted(pd.Series(_df["Dim1"]).dropna().astype(str).unique().tolist())
    if "Dim1" in _df.columns
    else []
)

# Total rows
n_rows = len(_df)

# ---------- Blocks ----------

# Problem statement
problem = dbc.Alert(
    [
        html.H5("Problem statement", className="mb-2"),
        html.P(
            "Have life expectancy gaps between regions of the world narrowed over "
            "the past 20 years, and do they differ between genders?"
        ),
    ],
    color="light",
    className="mb-4",
)

# KPIs
kpi_card_style = {"border": "none", "boxShadow": "0 2px 8px rgba(0,0,0,.06)"}
kpis = dbc.Row(
    [
        dbc.Col(
            dbc.Card(
                dbc.CardBody([html.H6("Countries"), html.H3(f"{n_countries}")]),
                style=kpi_card_style,
            ),
            md=3,
            xs=6,
        ),
        dbc.Col(
            dbc.Card(
                dbc.CardBody(
                    [
                        html.H6("Years range"),
                        html.H3(f"{year_min}–{year_max}" if year_min and year_max else "—"),
                    ]
                ),
                style=kpi_card_style,
            ),
            md=3,
            xs=6,
        ),
        dbc.Col(
            dbc.Card(
                dbc.CardBody(
                    [
                        html.H6("Sexes"),
                        html.H3(" · ".join(sexes) if sexes else "—"),
                    ]
                ),
                style=kpi_card_style,
            ),
            md=3,
            xs=6,
        ),
    ],
    className="g-3 mb-4",
)

# Objectives
objectives = dbc.Card(
    dbc.CardBody(
        [
            html.H4("Objectives", className="mb-3"),
            html.Ul(
                [
                    html.Li("Collect and clean public open data (WHO)."),
                    html.Li("Build a world choropleth map (countries / WHO regions)."),
                    html.Li("Analyze distributions with an interactive histogram."),
                    html.Li("Package everything into a small, reproducible Dash app."),
                ]
            ),
        ]
    ),
    className="mb-3",
)

# Data
data = dbc.Card(
    dbc.CardBody(
        [
            html.H4("Data", className="mb-3"),
            html.Ul(
                [
                    html.Li("Source: WHO — Life expectancy at birth (years)."),
                    html.Li(
                        "Key fields: TimeDim (year), Dim1 (sex), SpatialDim (ISO-3), "
                        "NumericValue (life expectancy), ParentLocation (region)."
                    ),
                    html.Li("Cleaning: keep COUNTRY rows, normalize sex labels, numeric coercion."),
                    html.Li("Boundaries: world countries GeoJSON; WHO regions GeoJSON (generated)."),
                ]
            ),
        ]
    ),
    className="mb-3",
)

# Tech stack
tech_stack = dbc.Card(
    dbc.CardBody(
        [
            html.H4("Tech stack", className="mb-3"),
            html.Ul(
                [
                    html.Li("Python 3.10+, Dash & Plotly, Dash Bootstrap Components."),
                    html.Li("Pandas for data prep, Folium for the choropleth."),
                ]
            ),
        ]
    ),
    className="mb-3",
)

# How to run
how_to_run = dbc.Card(
    dbc.CardBody(
        [
            html.H4("How to run", className="mb-3"),
            html.Ol(
                [
                    html.Li("Install deps:"),
                    html.Pre("python -m pip install -r requirements.txt"),
                    html.Li("Run the app:"),
                    html.Pre("python main.py"),
                    html.Li("Open the browser directly at this URL: http://127.0.0.1:8050/"),
                ]
            ),
        ]
    ),
    className="mb-3",
)

# Links & resources
links = dbc.Card(
    dbc.CardBody(
        [
            html.H4("Links & resources", className="mb-3"),
            html.Ul(
                [
                    html.Li(
                        html.A(
                            "WHO — GHO API (Life expectancy)",
                            href="https://www.who.int/data/gho/data/indicators/indicator-details/GHO/life-expectancy-at-birth-(years)",
                            target="_blank",
                        )
                    ),
                    html.Li(
                        html.A(
                            "Demo video",
                            href="https://…",
                            target="_blank",
                        )
                    ),
                ]
            ),
        ]
    ),
    className="mb-3",
)

# CTAs
cta = dbc.Row(
    [
        dbc.Col(dbc.Button("View Map", href="/map", color="primary"), width="auto"),
        dbc.Col(dbc.Button("View Histogram", href="/histogram", color="secondary"), width="auto"),
    ],
    className="g-2 mb-4",
)

# Credits & license — renamed from 'credits' to avoid redefinition
credits_section = dbc.Card(
    dbc.CardBody(
        [
            html.H4("Authors"),
            html.P(
                "Built by Keren Benadiba & Wilfried Lafaye (ESIEE Paris).",
            ),
            html.P(
                "This app is provided for educational purposes.",
            ),
            html.H6("Citation & license"),
            html.P(
                "If you use this app, please cite the WHO data source and this dashboard. "
                "Code released under the MIT License."
            ),
        ]
    ),
    className="mb-4",
)

# ---------- Page layout ----------
page_layout = dbc.Container(
    [
        html.H1("About this project", className="mt-4 mb-3"),
        problem,
        kpis,
        dbc.Row(
            [
                dbc.Col(objectives, md=6),
                dbc.Col(data, md=6),
            ],
            className="g-3",
        ),
        dbc.Row(
            [
                dbc.Col(tech_stack, md=6),
                dbc.Col(how_to_run, md=6),
            ],
            className="g-3",
        ),
        links,
        cta,
        credits_section,
    ],
    fluid=True,
    className="mb-5",
)
