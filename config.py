"""
Module de configuration de l'application Dashboard Life Expectancy.
Contient les chemins des fichiers de données et les URLs des API externes.
"""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_CSV = (
    '/workspaces/life-expectancy-dashboard/data/cleaned/cleaneddata.csv'
)

WORLD_GEOJSON_URL = (
    "https://raw.githubusercontent.com/johan/world.geo.json"
    "/master/countries.geo.json"
)
URL = "https://ghoapi.azureedge.net/api/WHOSIS_000001"
