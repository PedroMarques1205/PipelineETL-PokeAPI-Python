from dataclasses import dataclass
import pandas as pd
from datetime import date

@dataclass
class ExtractContract:
    raw_information_content: pd.DataFrame
    extraction_date: date