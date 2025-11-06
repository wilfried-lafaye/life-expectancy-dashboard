"""
Main module for the Life Expectancy Dashboard application.
"""

# Standard library imports
from pathlib import Path

# Third party imports
from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc

# Local application imports
from scripts.build_regional_geojson import create_who_regions_geojson
from src.utils.get_data import download_raw_data
from src.utils.clean_data import clean_data

# Download and clean data only if necessary
if not Path('data/raw/rawdata.csv').exists():
    download_raw_data()

if not Path('data/cleaned/cleaneddata.csv').exists():
    clean_data()

if not Path('data/raw/who_regions.geojson').exists():
    create_who_regions_geojson()

# Local application imports 2
from src.pages.home import page_layout as home_layout
from src.components.map import layout as map_layout
from src.components.histogram import layout as histogram_layout
from src.pages.about import page_layout as about_layout


# Application configuration
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP],
           suppress_callback_exceptions=True)
app.title = "Life Expectancy Dashboard"

app.layout = html.Div([
    dcc.Location(id="url"),
    dbc.NavbarSimple(
        children=[
            dbc.NavItem(dbc.NavLink("Home", href="/")),
            dbc.NavItem(dbc.NavLink("Map", href="/map")),
            dbc.NavItem(dbc.NavLink("Histogram", href="/histogram")),
            dbc.NavItem(dbc.NavLink("About", href="/about"))

        ],
        brand="Life Expectancy Dashboard",
        color="primary",
        dark=True,
    ),
    html.Div(id="page-content")
])

@app.callback(Output("page-content", "children"), Input("url", "pathname"))
def display_page(pathname):
    """
    Displays the appropriate page based on the URL pathname.

    Args:
        pathname (str): The current URL path.

    Returns:
        dash component: The layout corresponding to the selected page.
    """
    if pathname == "/map":
        return map_layout
    if pathname == "/histogram":
        return histogram_layout
    if pathname == "/about":
        return about_layout
    return home_layout

if __name__ == "__main__":
    app.run(debug=True)
