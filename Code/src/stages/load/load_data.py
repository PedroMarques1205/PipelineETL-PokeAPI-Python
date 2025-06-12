import os
import logging

from src.common.constants_utils import BASE_REPORTS_PATH
from src.common.graph_utils import GraphUtils
from src.stages.contract.transform_contract import TransformContract

logger = logging.getLogger(__name__)


class LoadData:

    def __init__(self, transform_contract: TransformContract):
        self.contract = transform_contract
        try:
            os.makedirs(BASE_REPORTS_PATH, exist_ok=True)
            logger.info(f"Diretório de relatórios garantido em: {BASE_REPORTS_PATH}")
        except Exception as e:
            logger.error(f"Erro ao criar diretório de relatórios: {e}")
            raise

    def export(self):
        logger.info("Iniciando processo de exportação dos dados...")
        try:
            self._export_top5_experiencia()
            self._export_media_status_por_tipo()
            self._export_graph()
            self._export_csv_consolidado()
            logger.info("Exportação concluída com sucesso.")
        except Exception as e:
            logger.exception("Erro durante o processo de exportação.")
            raise

    def _export_top5_experiencia(self):
        """
        Exporta os 5 Pokémons com maior experiência base para um arquivo CSV.
        """
        try:
            path = os.path.join(BASE_REPORTS_PATH, "top5_experiencia.csv")
            self.contract.top5_experiencia.to_csv(path, index=False)
            logger.info(f"Top 5 experiência exportado para: {path}")
        except Exception as e:
            logger.error(f"Erro ao exportar Top 5 experiência: {e}")
            raise

    def _export_media_status_por_tipo(self):
        """
        Exporta a média de ataque, defesa e HP por tipo de Pokémon para um arquivo CSV.
        """
        try:
            path = os.path.join(BASE_REPORTS_PATH, "media_status_por_tipo.csv")
            self.contract.media_status_por_tipo.to_csv(path, index=False)
            logger.info(f"Média de status por tipo exportada para: {path}")
        except Exception as e:
            logger.error(f"Erro ao exportar média de status por tipo: {e}")
            raise

    def _export_graph(self):
        """
        Gera e salva um gráfico de barras com a distribuição de Pokémons por tipo, utilizando os dados transformados.
        """
        try:
            path = GraphUtils.save_pokemon_type_distribution(self.contract.dataframe_por_tipo)
            logger.info(f"Gráfico de distribuição por tipo exportado para: {path}")
        except Exception as e:
            logger.error(f"Erro ao exportar gráfico de distribuição por tipo: {e}")
            raise

    def _export_csv_consolidado(self):
        """
        Exporta um relatório consolidado contendo o Top 5 por experiência e médias de status por tipo
        em um único arquivo CSV, com seções separadas e legíveis.
        """
        try:
            path = os.path.join(BASE_REPORTS_PATH, "consolidado.csv")
            with open(path, "w", encoding="utf-8") as f:
                f.write("Top 5 Pokémon com maior experiência base:\n")
                self.contract.top5_experiencia.to_csv(f, index=False)
                f.write("\n\nMédia de ataque, defesa e HP por tipo:\n")
                self.contract.media_status_por_tipo.to_csv(f, index=False)
            logger.info(f"CSV consolidado exportado para: {path}")
        except Exception as e:
            logger.error(f"Erro ao exportar CSV consolidado: {e}")
            raise
