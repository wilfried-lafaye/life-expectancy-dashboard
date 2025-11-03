"""
Module de nettoyage et préparation des données.
Ce script charge les données brutes, effectue un nettoyage
des colonnes et des lignes, supprime les colonnes vides,
et exporte les données nettoyées ainsi que les statistiques.
"""

import pandas as pd

def is_column_empty(series: pd.Series) -> bool:
    """
    Vérifie si une colonne est totalement vide (NaN ou chaînes vides).
    
    Args:
        series (pd.Series): La colonne du DataFrame à vérifier.
        
    Returns:
        bool: True si la colonne est vide, False sinon.
    """
    if series.dropna().empty:
        return True
    if series.dtype == 'object':
        non_empty = series.dropna().apply(lambda x: str(x).strip() != '')
        return not non_empty.any()
    return False

def clean_data():
    """
    Charge, nettoie et sauvegarde la DataFrame.
    """
    # Chargement des données
    df = pd.read_csv('data/raw/rawdata.csv')

    # Suppression des colonnes vides
    empty_cols = [col for col in df.columns if is_column_empty(df[col])]
    df = df.drop(columns=empty_cols)

    # Suppression des colonnes inutilisées
    unused_cols = [
        'TimeDimType', 'ParentLocationCode', 'TimeDimensionValue',
        'TimeDimensionBegin', 'TimeDimensionEnd', 'Date', 'Dim1Type',
        'Id', 'IndicatorCode', 'Low', 'High', 'Value'
    ]
    df = df.drop(columns=unused_cols)

    # Remappage de la colonne 'Dim1'
    corresponding_dict = {
        "SEX_BTSX": "Both",
        "SEX_MLE": "Male",
        "SEX_FMLE": "Female"
    }
    df['Dim1'] = df['Dim1'].map(corresponding_dict)

    # Sauvegarde du DataFrame nettoyé
    df.to_csv('data/cleaned/cleaneddata.csv', index=False)
