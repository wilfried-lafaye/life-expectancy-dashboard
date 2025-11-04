"""
Configuration module for the Life Expectancy Dashboard application.

Contains data file paths and external API URLs.
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

WHO_REGIONS_GEOJSON = '/workspaces/life-expectancy-dashboard/data/who_regions.geojson'

URL = "https://ghoapi.azureedge.net/api/WHOSIS_000001"
