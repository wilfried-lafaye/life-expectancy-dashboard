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

from config import DEFAULT_CSV, WORLD_GEOJSON_URL, WHO_REGIONS_GEOJSON, URL

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


def load_who_regions_geojson():
    """
    Loads the WHO regions GeoJSON file.
    
    Returns:
        dict: The WHO regions GeoJSON file content
    """
    with open(WHO_REGIONS_GEOJSON, 'r', encoding='utf-8') as f:
        return json.load(f)


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

    # Convert response to DataFrame
    data = response.json()
    df = pd.DataFrame(data['value'])

    # Save to CSV
    df.to_csv('data/raw/rawdata.csv', index=False)
    print('Data downloaded and saved in data/raw/rawdata.csv')
