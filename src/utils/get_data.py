"""
Data downloading and loading module.
Handles data downloading from the WHO API,
loading GeoJSON and cleaned data.
"""

import json
import sys
import urllib.request
from pathlib import Path

import pandas as pd
import requests

from config import DEFAULT_CSV, WORLD_GEOJSON_URL, URL

# Add project root to sys.path
ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(ROOT))


def load_world_geojson():
    """
    Loads the world countries GeoJSON file.

    Returns:
        dict: The GeoJSON file content
    """
    with urllib.request.urlopen(WORLD_GEOJSON_URL, timeout=15) as resp:
        gj = json.load(resp)
    return gj


def load_clean_data():
    """
    Loads cleaned data from the CSV file.

    Returns:
        pd.DataFrame: The cleaned data
    """
    return pd.read_csv(DEFAULT_CSV)


def download_raw_data():
    """
    Downloads raw data from the WHO API and saves it.

    Returns:
        None
    """
    # GET request to the API with timeout
    response = requests.get(URL, timeout=30)
    response.raise_for_status()

    # Convert response to JSON
    json_data = response.json()

    # Extract data from the 'value' key
    records = json_data.get('value', [])

    # Convert to pandas DataFrame
    df = pd.DataFrame.from_records(records)

    # Full path to save in data/raw/rawdata.csv
    output_path = "data/raw/rawdata.csv"

    # Save DataFrame to this CSV file without the index
    df.to_csv(output_path, index=False)
