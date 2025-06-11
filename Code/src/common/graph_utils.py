import os
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.container import BarContainer
import pandas as pd

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
        plt.figure(figsize=(10, 6))
        ax = sns.barplot(data=type_counts, x="Tipo", y="Quantidade", palette="viridis")

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

        return output_path

    @staticmethod
    def plot_pokemon_type_distribution(type_counts: pd.DataFrame):

        plt.figure(figsize=(10, 6))
        ax = sns.barplot(data=type_counts, x="Tipo", y="Quantidade", palette="viridis")

        for container in ax.containers:
            if isinstance(container, BarContainer):
                ax.bar_label(container, label_type="edge", padding=3, fontsize=10)

        plt.title("Distribuição de Pokémon por Tipo")
        plt.xlabel("Tipo")
        plt.ylabel("Quantidade")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()