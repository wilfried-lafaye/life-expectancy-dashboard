"""
Home page module - Landing page with navigation cards.
"""

from dash import html
import dash_bootstrap_components as dbc

page_layout = dbc.Container([
    html.H1("Life Expectancy Dashboard", className="text-center mt-5 mb-4"),
    html.P(
        "Explore global life expectancy data through interactive visualizations",
        className="text-center text-muted mb-5"
    ),
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4("🗺️ Interactive Map", className="card-title"),
                    html.P(
                        "Visualize life expectancy across countries and WHO regions "
                        "with an interactive choropleth map.",
                        className="card-text"
                    ),
                    dbc.Button("View Map", href="/map", color="primary")
                ])
            ], className="mb-4")
        ], md=6),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4("📊 Distribution Histogram", className="card-title"),
                    html.P(
                        "Analyze the distribution of countries by life expectancy ranges "
                        "over time.",
                        className="card-text"
                    ),
                    dbc.Button("View Histogram", href="/histogram", color="primary")
                ])
            ], className="mb-4")
        ], md=6),
    ], justify="center"),
], className="home-page", style={"marginTop": "2rem"})
