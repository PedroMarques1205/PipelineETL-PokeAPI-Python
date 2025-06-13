import os
import pytest
from unittest.mock import MagicMock, patch, mock_open
from src.stages.load.load_data import LoadData
from src.common.constants_utils import BASE_REPORTS_PATH

@pytest.fixture
def fake_contract():
    return MagicMock(
        top5_experiencia=MagicMock(),
        media_status_por_tipo=MagicMock(),
        dataframe_por_tipo=MagicMock()
    )

def test_init_cria_diretorio(fake_contract):
    with patch("os.makedirs") as makedirs_mock:
        LoadData(fake_contract)
        makedirs_mock.assert_called_once_with(BASE_REPORTS_PATH, exist_ok=True)

def test_export_chama_todos_metodos(fake_contract):
    loader = LoadData(fake_contract)
    with patch.object(loader, "_export_top5_experiencia") as m1, \
         patch.object(loader, "_export_media_status_por_tipo") as m2, \
         patch.object(loader, "_export_graph") as m3, \
         patch.object(loader, "_export_csv_consolidado") as m4:
        loader.export()
        m1.assert_called_once()
        m2.assert_called_once()
        m3.assert_called_once()
        m4.assert_called_once()

def test_export_top5_experiencia(fake_contract):
    loader = LoadData(fake_contract)
    path = os.path.join(BASE_REPORTS_PATH, "top5_experiencia.csv")
    loader._export_top5_experiencia()
    fake_contract.top5_experiencia.to_csv.assert_called_once_with(path, index=False)

def test_export_media_status_por_tipo(fake_contract):
    loader = LoadData(fake_contract)
    path = os.path.join(BASE_REPORTS_PATH, "media_status_por_tipo.csv")
    loader._export_media_status_por_tipo()
    fake_contract.media_status_por_tipo.to_csv.assert_called_once_with(path, index=False)

def test_export_graph(fake_contract):
    loader = LoadData(fake_contract)
    with patch("src.stages.load.load_data.GraphUtils.save_pokemon_type_distribution") as graph_mock:
        loader._export_graph()
        graph_mock.assert_called_once_with(fake_contract.dataframe_por_tipo)

def test_export_csv_consolidado(fake_contract):
    loader = LoadData(fake_contract)
    path = os.path.join(BASE_REPORTS_PATH, "consolidado.csv")
    m = mock_open()

    with patch("builtins.open", m):
        loader._export_csv_consolidado()

    m.assert_called_once_with(path, "w", encoding="utf-8")
    handle = m()
    handle.write.assert_any_call("Top 5 Pokémon com maior experiência base:\n")
    handle.write.assert_any_call("\n\nMédia de ataque, defesa e HP por tipo:\n")
    fake_contract.top5_experiencia.to_csv.assert_called_once_with(handle, index=False)
    fake_contract.media_status_por_tipo.to_csv.assert_called_once_with(handle, index=False)
