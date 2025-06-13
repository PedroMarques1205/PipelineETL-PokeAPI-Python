import pytest
import pandas as pd
from unittest.mock import MagicMock
from src.stages.transform.transform_raw_data import TransformData

@pytest.fixture
def mock_df():
    return pd.DataFrame({
        "Nome": ["Pikachu", "Bulbasaur", "Charizard", "Squirtle", "Mewtwo"],
        "Experiência Base": [112, 64, 240, 66, 300],
        "Tipos": [["Eletric"], ["Grass", "Poison"], ["Fire", "Flying"], ["Water"], ["Psychic"]],
        "HP": [35, 45, 78, 44, 106],
        "Ataque": [55, 49, 84, 48, 110],
        "Defesa": [40, 49, 78, 65, 90]
    })

@pytest.fixture
def transform_data(mock_df):
    mock_contract = MagicMock()
    mock_contract.raw_information_content = mock_df
    return TransformData(extract_data=mock_contract)

# Teste da classificação de categoria
def test_transform_data_classifying_pokemons(transform_data):
    df_result = transform_data.transform_data_classifying_pokemons()
    assert "Categoria" in df_result.columns
    assert df_result["Categoria"].tolist() == ["Forte", "Médio", "Forte", "Médio", "Forte"]

# Teste da contagem por tipo
def test_transform_count_pokemons_by_type(transform_data):
    df_result = transform_data.transform_count_pokemons_by_type()
    assert "Tipo" in df_result.columns
    assert "Quantidade" in df_result.columns
    tipos = df_result.set_index("Tipo")["Quantidade"].to_dict()
    assert tipos["Eletric"] == 1
    assert tipos["Grass"] == 1
    assert tipos["Poison"] == 1
    assert tipos["Fire"] == 1
    assert tipos["Flying"] == 1
    assert tipos["Water"] == 1
    assert tipos["Psychic"] == 1

# Teste das médias por tipo
def test_transform_stats_by_type(transform_data):
    df_result = transform_data.transform_stats_by_type()
    assert "Tipo" in df_result.columns
    assert "Média Ataque" in df_result.columns
    assert "Média Defesa" in df_result.columns
    assert "Média HP" in df_result.columns
    assert df_result[df_result["Tipo"] == "Eletric"]["Média Ataque"].iloc[0] == 55

# Teste do top 5
def test_transform_top5_base_experience(transform_data):
    df_result = transform_data.transform_top5_base_experience()
    assert list(df_result.columns) == ["Nome", "Experiência Base"]
    assert len(df_result) == 5
    assert df_result.iloc[0]["Experiência Base"] == 300  # Mewtwo

# Teste da função estática de classificação isoladamente
@pytest.mark.parametrize("exp, esperado", [
    (30, "Fraco"),
    (75, "Médio"),
    (120, "Forte"),
    (None, "Desconhecido"),
])
def test_classify_pokemon_strength(exp, esperado):
    resultado = TransformData.classify_pokemon_strength(exp)
    assert resultado == esperado
