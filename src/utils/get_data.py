"""
Module de téléchargement et chargement des données.
Gère le téléchargement des données depuis l'API WHO,
le chargement du GeoJSON et des données nettoyées.
"""

import json
import sys
import urllib.request
from pathlib import Path

import pandas as pd
import requests

from config import DEFAULT_CSV, WORLD_GEOJSON_URL, URL

# ajoute la racine du projet au sys.path
ROOT = Path(__file__).resolve().parents[2]
sys.path.append(str(ROOT))


def load_world_geojson():
    """
    Charge le fichier GeoJSON des pays du monde.

    Returns:
        dict: Le contenu du fichier GeoJSON
    """
    with urllib.request.urlopen(WORLD_GEOJSON_URL, timeout=15) as resp:
        gj = json.load(resp)
    return gj


def load_clean_data():
    """
    Charge les données nettoyées depuis le fichier CSV.

    Returns:
        pd.DataFrame: Les données nettoyées
    """
    return pd.read_csv(DEFAULT_CSV)


def download_raw_data():
    """
    Télécharge les données brutes depuis l'API WHO et les sauvegarde.

    Returns:
        None
    """
    # Requête GET vers l'API avec timeout
    response = requests.get(URL, timeout=30)
    response.raise_for_status()

    # Conversion de la réponse en JSON
    json_data = response.json()

    # Extraction des données dans la clé 'value'
    records = json_data.get('value', [])

    # Conversion en DataFrame pandas
    df = pd.DataFrame.from_records(records)

    # Chemin complet pour sauvegarder dans data/raw/rawdata.csv
    output_path = "data/raw/rawdata.csv"

    # Sauvegarde du DataFrame dans ce fichier CSV sans l'index
    df.to_csv(output_path, index=False)
