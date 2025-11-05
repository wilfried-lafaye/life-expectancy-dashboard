"""
Data cleaning and preparation module.

This script loads the raw data, performs cleaning
on columns and rows, removes empty columns,
and exports the cleaned data as well as statistics.
"""

import pandas as pd

def is_column_empty(series: pd.Series) -> bool:
    """
    Checks if a column is completely empty (NaN or empty strings).

    Args:
        series (pd.Series): The DataFrame column to check.

    Returns:
        bool: True if the column is empty, False otherwise.
    """
    if series.dropna().empty:
        return True
    if series.dtype == 'object':
        non_empty = series.dropna().apply(lambda x: str(x).strip() != '')
        return not non_empty.any()
    return False

def clean_data():
    """
    Loads, cleans, and saves the DataFrame.
    """
    # Load data
    df = pd.read_csv('data/raw/rawdata.csv')

    # Remove empty columns
    empty_cols = [col for col in df.columns if is_column_empty(df[col])]
    df = df.drop(columns=empty_cols)

    # Remove unused columns
    unused_cols = [
        'TimeDimType', 'ParentLocationCode', 'TimeDimensionValue',
        'TimeDimensionBegin', 'TimeDimensionEnd', 'Date', 'Dim1Type',
        'Id', 'IndicatorCode', 'Low', 'High', 'Value', 'ParentLocation'
    ]
    df = df.drop(columns=unused_cols)

    # Remap the 'Dim1' column
    corresponding_dict = {
        "SEX_BTSX": "Both",
        "SEX_MLE": "Male",
        "SEX_FMLE": "Female"
    }
    df['Dim1'] = df['Dim1'].map(corresponding_dict)

    # Save the cleaned DataFrame
    df.to_csv('data/cleaned/cleaneddata.csv', index=False)
