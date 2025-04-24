import pandas as pd
import numpy as np
import requests
from pyjstat import pyjstat
from datetime import datetime
import os
from config import *

def extract_data_from_bank_pt(series_id, variable_name):
    """
    Function to extract data from BPSTAT API.

    Arguments: series_id int
             variable_name str.
             If variable_name is None, variable_name is set to urls label.

    Returns:   pandas dataframe with Date and variable_name columns
    """

    BPSTAT_API_URL = "https://bpstat.bportugal.pt/data/v1"

    url = f"{BPSTAT_API_URL}/series/?lang=EN&series_ids={series_id}"
    series_info = requests.get(url).json()[0]

    print(f"Extracting data from BPSTAT API...{series_id}")

    domain_id = series_info["domain_ids"][0]
    dataset_id = series_info["dataset_id"]

    dataset_url = f"{BPSTAT_API_URL}/domains/{domain_id}/datasets/{dataset_id}/?lang=EN&series_ids={series_id}"
    dataset = pyjstat.Dataset.read(dataset_url)
    df = dataset.write('dataframe')

    df['Date'] = pd.to_datetime(df['Date'])
    if variable_name is None:
        variable_name = series_info['label']

    df = df.rename(columns={'value': variable_name})
    df = df[['Date', variable_name]]
    df['Date'] = pd.to_datetime(df['Date']).dt.date

    return df

def get_emfs_data(dict_indicator_keys):
    """Extrai dados do bpstat sem multiindex"""
    ano_atual = datetime.now().year - 1

    df_final = pd.DataFrame()
    df_final['Date'] = pd.date_range(start='2006-12-31', end=f'{ano_atual}-12-31', freq='A-DEC')

    for series_id, series_name in dict_indicator_keys.items():
        df_extracted = extract_data_from_bank_pt(series_id, None)
        df_extracted['Date'] = pd.to_datetime(df_extracted['Date'])
        
        df_final = df_final.merge(df_extracted, on='Date', how='left')

    df_final.to_csv("Data/emfs.csv")
    print("Dados atualizados com sucesso!")


if __name__ == "__main__":
    from config import bank_pt_series_dict
    get_emfs_data(bank_pt_series_dict)
