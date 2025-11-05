"""
Main module for the Life Expectancy Dashboard application.
"""
# Data pipeline
from src.utils.get_data import download_raw_data
from src.utils.clean_data import clean_data
from scripts.create_who_regions import create_who_regions_geojson
from pathlib import Path


# Download and clean data only if necessary
if not Path('data/raw/who_regions.geojson').exists():
    create_who_regions_geojson()

if not Path('data/raw/rawdata.csv').exists():
    download_raw_data()
    
if not Path('data/cleaned/cleaneddata.csv').exists():
    clean_data()

from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc

# Import page layouts
from src.pages.home import page_layout as home_layout
from src.components.map import layout as map_layout
from src.components.histogram import layout as histogram_layout

# Application configuration
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)
app.title = "Life Expectancy Dashboard"

app.layout = html.Div([
    dcc.Location(id="url"),
    dbc.NavbarSimple(
        children=[
            dbc.NavItem(dbc.NavLink("Home", href="/")),
            dbc.NavItem(dbc.NavLink("Map", href="/map")),
            dbc.NavItem(dbc.NavLink("Histogram", href="/histogram"))
        ],
        brand="Life Expectancy Dashboard",
        color="primary", 
        dark=True,
    ),
    html.Div(id="page-content")
])

@app.callback(Output("page-content", "children"), Input("url", "pathname"))
def display_page(pathname):
    if pathname == "/map":
        return map_layout
    elif pathname == "/histogram":
        return histogram_layout
    else:
        return home_layout

if __name__ == "__main__":
    app.run(debug=True)
