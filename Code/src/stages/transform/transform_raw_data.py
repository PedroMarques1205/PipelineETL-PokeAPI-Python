import pandas as pd

from src.common.graph_utils import GraphUtils
from src.stages.contract.extract_contract import ExtractContract
from src.stages.contract.transform_contract import TransformContract


class TransformData:

    def __init__(self, extract_data: ExtractContract):
        self.__extract_data = extract_data


    def transform(self) -> TransformContract:
        df_classificado = self.transform_data_classifying_pokemons()
        df_tipos = self.transform_count_pokemons_by_type()
        df_media = self.transform_stats_by_type()
        df_top5 = self.transform_top5_base_experience()

        GraphUtils.plot_pokemon_type_distribution(df_tipos)

        return TransformContract(
            dataframe_classificado=df_classificado,
            dataframe_por_tipo=df_tipos,
            media_status_por_tipo=df_media,
            top5_experiencia=df_top5,
        )


    def transform_data_classifying_pokemons(self):
        extracted_data = self.__extract_data.raw_information_content
        extracted_data["Experiência Base"] = pd.to_numeric(extracted_data["Experiência Base"], errors="coerce")
        extracted_data["Categoria"] = extracted_data["Experiência Base"].apply(self.classify_pokemon_strength)
        return extracted_data


    def transform_count_pokemons_by_type(self) -> pd.DataFrame:
        extracted_data = self.__extract_data.raw_information_content
        exploded = extracted_data.explode("Tipos")
        type_counts = exploded["Tipos"].value_counts().reset_index()
        type_counts.columns = ["Tipo", "Quantidade"]
        return type_counts


    def transform_stats_by_type(self) -> pd.DataFrame:
        df = self.__extract_data.raw_information_content.copy()
        df = df.explode("Tipos")
        grouped = df.groupby("Tipos")[["Ataque", "Defesa", "HP"]].mean().reset_index()
        grouped.columns = ["Tipo", "Média Ataque", "Média Defesa", "Média HP"]
        return grouped


    def transform_top5_base_experience(self) -> pd.DataFrame:
        df = self.__extract_data.raw_information_content.copy()
        df["Experiência Base"] = pd.to_numeric(df["Experiência Base"], errors="coerce")
        df_sorted = df.sort_values("Experiência Base", ascending=False)
        top5 = df_sorted[["Nome", "Experiência Base"]].head(5)
        return top5


    @staticmethod
    def classify_pokemon_strength(exp: float) -> str:
        if exp < 50:
            return "Fraco"
        elif 50 <= exp <= 100:
            return "Médio"
        else:
            return "Forte"