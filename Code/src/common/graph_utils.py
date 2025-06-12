import os
import logging
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.container import BarContainer
import pandas as pd

# Logger da classe
logger = logging.getLogger(__name__)


class GraphUtils:

    @staticmethod
    def save_pokemon_type_distribution(
        type_counts: pd.DataFrame,
        output_path: str = "reports/type_distribution.png"
    ) -> str:
        """
        Gera e salva um gráfico de barras com a distribuição de pokémons por tipo.

        :param type_counts: DataFrame com colunas ['Tipo', 'Quantidade']
        :param output_path: Caminho onde a imagem será salva
        :return: Caminho da imagem salva
        """
        try:
            logger.info("Iniciando geração do gráfico de distribuição de Pokémon por tipo.")
            plt.figure(figsize=(10, 6))
            ax = sns.barplot(
                data=type_counts,
                x="Tipo",
                y="Quantidade",
                hue="Tipo",
                palette="viridis",
                legend=False
            )

            for container in ax.containers:
                if isinstance(container, BarContainer):
                    ax.bar_label(container, label_type="edge", padding=3, fontsize=10)

            plt.title("Distribuição de Pokémon por Tipo")
            plt.xlabel("Tipo")
            plt.ylabel("Quantidade")
            plt.xticks(rotation=45)
            plt.tight_layout()

            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            plt.savefig(output_path, dpi=300, bbox_inches="tight")
            plt.close()

            logger.info(f"Gráfico salvo com sucesso em: {output_path}")
            return output_path

        except Exception as e:
            logger.error(f"Erro ao salvar gráfico de distribuição: {e}")
            raise

    @staticmethod
    def plot_pokemon_type_distribution(type_counts: pd.DataFrame):
        plt.figure(figsize=(10, 6))
        ax = sns.barplot(data=type_counts, x="Tipo", y="Quantidade", palette="viridis", legend=False, hue=True)

        for container in ax.containers:
            if isinstance(container, BarContainer):
                ax.bar_label(container, label_type="edge", padding=3, fontsize=10)

        plt.title("Distribuição de Pokémon por Tipo")
        plt.xlabel("Tipo")
        plt.ylabel("Quantidade")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()
