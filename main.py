"""
Module principal de l'application Dashboard Life Expectancy.
Ce module initialise l'application Dash, télécharge et nettoie les données,
puis configure les routes et callbacks.
"""

from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc

# Pipeline de données
from src.utils.get_data import download_raw_data
from src.utils.clean_data import clean_data
from src.pages.home import page_layout, register_callbacks
from src.components.histogramme import layout as histogram_layout


# Téléchargement et nettoyage des données
download_raw_data()
clean_data()


# Configuration de l'application
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)
app.title = "Dashboard"


app.layout = html.Div([
    dcc.Location(id="url"),
    dbc.NavbarSimple(
        children=[
            dbc.NavItem(dbc.NavLink("Carte", href="/")),
            dbc.NavItem(dbc.NavLink("Histogramme", href="/histogram"))
        ],
        brand="Life Expectancy Dashboard",
        color="primary", dark=True,
    ),
    html.Div(id="page-content")
])


@app.callback(Output("page-content", "children"), Input("url", "pathname"))
def render_page(pathname):
    """
    Callback pour afficher la page appropriée selon l'URL.
    
    Args:
        pathname (str): Le chemin de l'URL courante
        
    Returns:
        Component: Le layout de la page correspondante
    """
    if pathname == "/histogram":
        return histogram_layout
    return page_layout


register_callbacks(app)


if __name__ == "__main__":
    app.run(debug=True, port=8052)
