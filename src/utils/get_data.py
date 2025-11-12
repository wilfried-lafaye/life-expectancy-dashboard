"""
Data downloading and loading module.

Handles data downloading from the WHO API,
loading GeoJSON and cleaned data,
and verifying availability of external resources.
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


def check_url_availability(url: str, timeout: int = 10) -> bool:
    """Check if a remote URL is accessible (HTTP 200)."""
    try:
        response = requests.head(url, timeout=timeout)
        return response.status_code == 200
    except requests.RequestException:
        return False


def check_all_resources_available() -> bool:
    """Check availability of all important external URLs."""
    urls = [WORLD_GEOJSON_URL, URL]
    return all(check_url_availability(u) for u in urls)


def load_world_geojson() -> dict:
    """Load the world countries GeoJSON file."""
    with urllib.request.urlopen(WORLD_GEOJSON_URL, timeout=15) as resp:
        return json.load(resp)


def load_who_regions_geojson() -> dict:
    """Load the WHO regions GeoJSON file."""
    with open(WHO_REGIONS_GEOJSON, "r", encoding="utf-8") as file:
        return json.load(file)


def load_clean_data() -> pd.DataFrame:
    """Load cleaned data from CSV file."""
    return pd.read_csv(DEFAULT_CSV)


def download_raw_data() -> None:
    """
    Download raw data from the WHO API and save it locally.
    Checks URL availability before downloading.
    """
    if not check_url_availability(URL):
        print(f"Error: API URL not reachable: {URL}")
        return

    response = requests.get(URL, timeout=30)
    response.raise_for_status()

    data = response.json()
    df = pd.DataFrame(data["value"])

    csv_path = Path("data/raw/rawdata.csv")
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(csv_path, index=False)
    print(f"Data downloaded and saved in {csv_path}")
