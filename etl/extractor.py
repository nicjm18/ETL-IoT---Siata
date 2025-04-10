import requests
import pandas as pd

def extraer_datos(url: str) -> pd.DataFrame:
    response = requests.get(url)
    data = response.json()
    return pd.json_normalize(data['measurements'])
