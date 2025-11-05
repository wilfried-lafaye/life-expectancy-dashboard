"""
Home page module - Landing page with project overview.
"""
from dash import html
import dash_bootstrap_components as dbc

page_layout = dbc.Container([
    html.H1("Life Expectancy Dashboard", className="my-4"),
    html.P("Explore global life expectancy data from the WHO."),
    
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4("🗺️ Interactive Map", className="card-title"),
                    html.P("Visualize life expectancy by country or WHO region"),
                    dbc.Button("Go to Map", href="/map", color="primary")
                ])
            ])
        ], width=6),
        
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4("📊 Histogram Analysis", className="card-title"),
                    html.P("See distribution of countries by life expectancy ranges"),
                    dbc.Button("Go to Histogram", href="/histogram", color="primary")
                ])
            ])
        ], width=6)
    ])
], className="my-5")

def register_callbacks(app):
    """No callbacks needed for static home page."""
    pass
