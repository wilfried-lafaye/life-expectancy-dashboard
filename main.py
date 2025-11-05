"""
Main module for the Life Expectancy Dashboard application.
This module initializes the Dash application, downloads and cleans the data,
then configures routes and callbacks.
"""


# Data pipeline
from pathlib import Path
from src.utils.get_data import download_raw_data
from src.utils.clean_data import clean_data


# Download and clean data only if necessary
if not Path('data/raw/rawdata.csv').exists():
    download_raw_data()
    
if not Path('data/cleaned/cleaneddata.csv').exists():
    clean_data()


from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc


from src.pages.home import page_layout, register_callbacks
from src.components.histogramme import layout as histogram_layout



# Application configuration
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)
app.title = "Dashboard"



app.layout = html.Div([
    dcc.Location(id="url"),
    dbc.NavbarSimple(
        children=[
            dbc.NavItem(dbc.NavLink("Map", href="/map")),
            dbc.NavItem(dbc.NavLink("Histogram", href="/histogram"))
        ],
        brand="Life Expectancy Dashboard",
        color="primary", dark=True,
    ),
    html.Div(id="page-content")
])



@app.callback(Output("page-content", "children"), Input("url", "pathname"))
def render_page(pathname):
    """
    Callback to display the appropriate page based on the URL.
    
    Args:
        pathname (str): The current URL path
        
    Returns:
        Component: The corresponding page layout
    """
    if pathname == "/histogram":
        return histogram_layout
    return page_layout



register_callbacks(app)



if __name__ == "__main__":
    app.run(debug=True, port=8052)
