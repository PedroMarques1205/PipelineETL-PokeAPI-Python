import pandas as pd
from src.stages.contract.extract_contract import ExtractContract

class TransformData:

    def __init__(self, extract_data: ExtractContract):
        self.__extract_data = extract_data


    def transform(self):
        self.transform_data_classifying_pokemons()


    def transform_data_classifying_pokemons(self):
        extracted_data = self.__extract_data.raw_information_content

        extracted_data["Experiência Base"] = pd.to_numeric(extracted_data["Experiência Base"], errors="coerce")

        extracted_data["Categoria"] = extracted_data["Experiência Base"].apply(self.classify_pokemon_strength)

        return extracted_data


    @staticmethod
    def classify_pokemon_strength(exp: float) -> str:
        if exp < 50:
            return "Fraco"
        elif 50 <= exp <= 100:
            return "Médio"
        else:
            return "Forte"