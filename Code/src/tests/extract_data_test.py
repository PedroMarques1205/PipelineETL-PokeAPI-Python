from unittest.mock import MagicMock, patch
from datetime import date
from src.stages.extract.extract_data import ExtractData
from src.stages.contract.extract_contract import ExtractContract

def test_extract_data_retorna_contract():
    fake_data = [{"name": "pikachu"}]
    fake_dataframe = "df_mockado"
    fake_requester = MagicMock()
    fake_requester.request_pokemon_details.return_value = fake_data

    with patch("src.stages.extract.extract_data.DataCollector") as mock_collector:
        mock_instance = mock_collector.return_value
        mock_instance.build_dataframe.return_value = fake_dataframe

        extractor = ExtractData(fake_requester)

        result = extractor.extract()

        fake_requester.request_pokemon_details.assert_called_once()
        mock_collector.assert_called_once_with(fake_data)
        mock_instance.build_dataframe.assert_called_once()

        assert isinstance(result, ExtractContract)
        assert result.raw_information_content == fake_dataframe
        assert result.extraction_date == date.today()
