"""
Main module for the Life Expectancy Dashboard application.

This module initializes the Dash application, downloads and cleans the data,
then configures routes and callbacks.
"""

import sys
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('dashboard.log', mode='a', encoding='utf-8')
    ]
)
logger = logging.getLogger(__name__)


def initialize_data_pipeline():
    """
    Initialize the data pipeline by downloading and processing data.

    Returns:
        bool: True if successful, False otherwise
    """
    from src.utils.get_data import download_raw_data
    from src.utils.clean_data import clean_data
    from src.utils.create_who_regions import create_who_regions_geojson

    logger.info("=" * 60)
    logger.info("Starting data pipeline initialization...")
    logger.info("=" * 60)

    logger.info("Step 1/3: Downloading raw data from WHO API...")
    download_raw_data()
    logger.info("✓ Raw data downloaded successfully")

    logger.info("Step 2/3: Cleaning and processing data...")
    clean_data()
    logger.info("✓ Data cleaned successfully")

    logger.info("Step 3/3: Creating WHO regions GeoJSON...")
    create_who_regions_geojson()
    logger.info("✓ WHO regions GeoJSON created successfully")

    logger.info("=" * 60)
    logger.info("✓ Data pipeline initialized successfully")
    logger.info("=" * 60)
    return True


def create_dash_app():
    """
    Create and configure the Dash application.

    Returns:
        Dash: The configured Dash application instance
    """
    from dash import Dash, dcc, html, Input, Output
    import dash_bootstrap_components as dbc
    from src.pages.home import page_layout, register_callbacks
    from src.components.histogramme import layout as histogram_layout

    logger.info("Creating Dash application...")

    app = Dash(
        __name__,
        external_stylesheets=[dbc.themes.BOOTSTRAP],
        suppress_callback_exceptions=True
    )
    app.title = "Life Expectancy Dashboard"

    app.layout = html.Div([
        dcc.Location(id="url"),
        dbc.NavbarSimple(
            children=[
                dbc.NavItem(dbc.NavLink("Map", href="/map")),
                dbc.NavItem(dbc.NavLink("Histogram", href="/histogram"))
            ],
            brand="Life Expectancy Dashboard",
            color="primary",
            dark=True,
        ),
        html.Div(id="page-content")
    ])

    @app.callback(
        Output("page-content", "children"),
        Input("url", "pathname")
    )
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
        if pathname in ("/map", "/", None):
            return page_layout
        
        return html.Div([
            html.H3("404 - Page Not Found"),
            html.P(f"The page '{pathname}' does not exist."),
            dbc.Button("Go to Map", href="/map", color="primary")
        ], style={"textAlign": "center", "marginTop": "50px"})

    register_callbacks(app)
    logger.info("✓ Dash application created successfully")
    return app


def main():
    """Main entry point for the application."""
    try:
        logger.info("Starting Life Expectancy Dashboard application...")
        
        initialize_data_pipeline()
        app = create_dash_app()
        
        logger.info("=" * 60)
        logger.info("Starting Dash server on http://127.0.0.1:8051/")
        logger.info("Press CTRL+C to stop the server")
        logger.info("=" * 60)
        
        app.run(debug=True, port=8051)
    
    except KeyboardInterrupt:
        logger.info("\n" + "=" * 60)
        logger.info("Server stopped by user (CTRL+C)")
        logger.info("=" * 60)
        sys.exit(0)
    
    except Exception as exc:
        logger.error("Critical error: %s", exc)
        sys.exit(1)


if __name__ == "__main__":
    main()
