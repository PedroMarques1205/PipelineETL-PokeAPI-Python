import pandas as pd
from dataclasses import dataclass

@dataclass
class TransformContract:
    dataframe_classificado: pd.DataFrame
    dataframe_por_tipo: pd.DataFrame
    media_status_por_tipo: pd.DataFrame
    top5_experiencia: pd.DataFrame