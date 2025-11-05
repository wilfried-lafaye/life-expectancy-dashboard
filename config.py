"""
Configuration module for the Life Expectancy Dashboard application.
Contains data file paths and external API URLs.
"""

from pathlib import Path

# Project root (where config.py is located)
ROOT = Path(__file__).resolve().parent

# Data directories
DATA_DIR = ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
CLEANED_DATA_DIR = DATA_DIR / "cleaned"

# File paths (relative)
RAW_DATA_CSV = RAW_DATA_DIR / "rawdata.csv"
DEFAULT_CSV = CLEANED_DATA_DIR / "cleaneddata.csv"
WHO_REGIONS_GEOJSON = DATA_DIR / "who_regions.geojson"

# External URLs
WORLD_GEOJSON_URL = (
    "https://raw.githubusercontent.com/johan/world.geo.json"
    "/master/countries.geo.json"
)

URL = "https://ghoapi.azureedge.net/api/WHOSIS_000001"
