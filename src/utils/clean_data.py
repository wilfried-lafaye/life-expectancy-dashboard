"""
Module de nettoyage et préparation des données.
Ce script charge les données brutes, effectue un nettoyage
des colonnes et des lignes, supprime les colonnes vides,
et exporte les données nettoyées ainsi que les statistiques descriptives.
"""

import pandas as pd

# =============================================================
# FONCTION PRINCIPALE DE NETTOYAGE
# =============================================================

def clean_data():
    # Chargement des données
    RAW_DATA_PATH = 'data/raw/rawdata.csv'
    df = pd.read_csv(RAW_DATA_PATH)

    # Fonction utilitaire
    def is_column_empty(series: pd.Series) -> bool:
        """Vérifie si une colonne est entièrement vide (NaN ou chaînes vides)."""
        if series.dropna().empty:
            return True
        if series.dtype == 'object':
            non_empty = series.dropna().apply(lambda x: str(x).strip() != '')
            return not non_empty.any()
        return False

    # Suppression des colonnes vides
    empty_cols = [col for col in df.columns if is_column_empty(df[col])]
    df = df.drop(columns=empty_cols)

    # Suppression des colonnes inutilisées spécifiques
    unused_cols = [
        'TimeDimType',
        'ParentLocationCode',
        'TimeDimensionValue',
        'TimeDimensionBegin',
        'TimeDimensionEnd',
        'Date',
        'Dim1Type',
        'Id',
        'IndicatorCode',
        'Low',
        'High',
        'Value'
    ]
    df = df.drop(columns=unused_cols)

    # Remappage values de la colonne 'Dim1'
    corresponding_dict = {
        "SEX_BTSX": "Both",
        "SEX_MLE": "Male",
        "SEX_FMLE": "Female",
    }
    df['Dim1'] = df['Dim1'].map(corresponding_dict)

    # Sauvegarde du fichier nettoyé
    df.to_csv('data/cleaned/cleaneddata.csv', index=False)
