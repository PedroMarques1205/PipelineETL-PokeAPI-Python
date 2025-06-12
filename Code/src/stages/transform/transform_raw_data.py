import logging
import pandas as pd

from src.common.graph_utils import GraphUtils
from src.stages.contract.extract_contract import ExtractContract
from src.stages.contract.transform_contract import TransformContract

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TransformData:

    def __init__(self, extract_data: ExtractContract):
        self.__extract_data = extract_data

    def transform(self) -> TransformContract:
        logger.info("Iniciando transformação completa dos dados.")
        try:
            df_classificado = self.transform_data_classifying_pokemons()
            df_tipos = self.transform_count_pokemons_by_type()
            df_media = self.transform_stats_by_type()
            df_top5 = self.transform_top5_base_experience()

            logger.info("Gerando gráfico de distribuição de tipos de Pokémon.")
            try:
                GraphUtils.plot_pokemon_type_distribution(df_tipos)
            except Exception as e:
                logger.error(f"Erro ao gerar gráfico de distribuição: {e}")
                raise

            logger.info("Transformações finalizadas com sucesso.")
            return TransformContract(
                dataframe_classificado=df_classificado,
                dataframe_por_tipo=df_tipos,
                media_status_por_tipo=df_media,
                top5_experiencia=df_top5,
            )
        except Exception as e:
            logger.exception("Erro durante a transformação dos dados.")
            raise

    def transform_data_classifying_pokemons(self):
        """
        Classifica os Pokémons com base na experiência base.
        - Converte a coluna 'Experiência Base' para numérica.
        - Adiciona uma nova coluna 'Categoria' com a classificação:
            - "Fraco" para experiência < 50
            - "Médio" para experiência entre 50 e 100
            - "Forte" para experiência > 100
        :return: DataFrame atualizado com a coluna 'Categoria'.
        :raises Exception: Em caso de erro na classificação.
        """
        logger.info("Classificando Pokémons por experiência base.")
        try:
            extracted_data = self.__extract_data.raw_information_content
            extracted_data["Experiência Base"] = pd.to_numeric(extracted_data["Experiência Base"], errors="coerce")
            extracted_data["Categoria"] = extracted_data["Experiência Base"].apply(self.classify_pokemon_strength)
            logger.info("Classificação concluída.")
            return extracted_data
        except Exception as e:
            logger.error(f"Erro ao classificar Pokémons por experiência base: {e}")
            raise

    def transform_count_pokemons_by_type(self) -> pd.DataFrame:
        """
        Conta a quantidade de Pokémons por tipo.

            - Explode os tipos (lista de tipos por Pokémon) em múltiplas linhas.
            - Agrupa por tipo e conta a ocorrência de cada um.

        :return: DataFrame com as colunas ['Tipo', 'Quantidade'].
        :raises Exception: Em caso de erro no agrupamento ou contagem.
        """
        logger.info("Contando Pokémons por tipo.")
        try:
            extracted_data = self.__extract_data.raw_information_content
            exploded = extracted_data.explode("Tipos")
            type_counts = exploded["Tipos"].value_counts().reset_index()
            type_counts.columns = ["Tipo", "Quantidade"]
            logger.info("Contagem por tipo concluída.")
            return type_counts
        except Exception as e:
            logger.error(f"Erro ao contar Pokémons por tipo: {e}")
            raise

    def transform_stats_by_type(self) -> pd.DataFrame:
        """
        Calcula as médias dos atributos 'Ataque', 'Defesa' e 'HP' para cada tipo de Pokémon.
           - Explode os tipos para que cada tipo seja considerado individualmente.
           - Agrupa por tipo e calcula as médias dos atributos citados.

           :return: DataFrame com as colunas ['Tipo', 'Média Ataque', 'Média Defesa', 'Média HP'].
           :raises Exception: Em caso de erro durante o cálculo das médias.
        """

        logger.info("Calculando médias de status (Ataque, Defesa, HP) por tipo.")
        try:
            df = self.__extract_data.raw_information_content.copy()
            df = df.explode("Tipos")
            grouped = df.groupby("Tipos")[["Ataque", "Defesa", "HP"]].mean().reset_index()
            grouped.columns = ["Tipo", "Média Ataque", "Média Defesa", "Média HP"]
            logger.info("Médias por tipo calculadas.")
            return grouped
        except Exception as e:
            logger.error(f"Erro ao calcular médias por tipo: {e}")
            raise

    def transform_top5_base_experience(self) -> pd.DataFrame:
        """
        Seleciona os 5 Pokémons com maior valor de experiência base.

           - Converte a coluna 'Experiência Base' para numérica.
           - Ordena os Pokémons de forma decrescente por experiência base.
           - Seleciona os 5 primeiros.

        :return: DataFrame com as colunas ['Nome', 'Experiência Base'] dos top 5.
        :raises Exception: Em caso de erro na ordenação ou seleção.
        """

        logger.info("Selecionando os 5 Pokémons com maior experiência base.")
        try:
            df = self.__extract_data.raw_information_content.copy()
            df["Experiência Base"] = pd.to_numeric(df["Experiência Base"], errors="coerce")
            df_sorted = df.sort_values("Experiência Base", ascending=False)
            top5 = df_sorted[["Nome", "Experiência Base"]].head(5)
            logger.info("Top 5 selecionado.")
            return top5
        except Exception as e:
            logger.error(f"Erro ao selecionar Top 5 por experiência base: {e}")
            raise

    @staticmethod
    def classify_pokemon_strength(exp: float) -> str:
        try:
            if exp < 50:
                return "Fraco"
            elif 50 <= exp <= 100:
                return "Médio"
            else:
                return "Forte"
        except Exception as e:
            logger.error(f"Erro ao classificar força do Pokémon: {e}")
            return "Desconhecido"
