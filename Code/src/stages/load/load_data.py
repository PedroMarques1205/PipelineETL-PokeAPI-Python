import os

from src.common.constants_utils import BASE_REPORTS_PATH
from src.common.graph_utils import GraphUtils
from src.stages.contract.transform_contract import TransformContract


class LoadData:

    def __init__(self, transform_contract: TransformContract):
        self.contract = transform_contract
        os.makedirs(BASE_REPORTS_PATH, exist_ok=True)

    def export(self):
        self._export_top5_experiencia()
        self._export_media_status_por_tipo()
        self._export_graph()
        self._export_csv_consolidado()

    def _export_top5_experiencia(self):
        path = os.path.join(BASE_REPORTS_PATH, "top5_experiencia.csv")
        self.contract.top5_experiencia.to_csv(path, index=False)

    def _export_media_status_por_tipo(self):
        path = os.path.join(BASE_REPORTS_PATH, "media_status_por_tipo.csv")
        self.contract.media_status_por_tipo.to_csv(path, index=False)

    def _export_graph(self):
        GraphUtils.save_pokemon_type_distribution(self.contract.dataframe_por_tipo)

    def _export_csv_consolidado(self):
        path = os.path.join(BASE_REPORTS_PATH, "consolidado.csv")
        with open(path, "w", encoding="utf-8") as f:
            f.write("Top 5 Pokémon com maior experiência base:\n")
            self.contract.top5_experiencia.to_csv(f, index=False)
            f.write("\n\nMédia de ataque, defesa e HP por tipo:\n")
            self.contract.media_status_por_tipo.to_csv(f, index=False)