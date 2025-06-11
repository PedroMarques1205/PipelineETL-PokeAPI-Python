from src.common.constants_utils import LOGGER_FORMAT

import logging

from src.drivers.api_requester import ApiRequester
from src.stages.extract.extract_data import ExtractData
from src.stages.load.load_data import LoadData
from src.stages.transform.transform_raw_data import TransformData

logging.basicConfig(
    level=logging.INFO,
    format=LOGGER_FORMAT
)

def main():
    extract = ExtractData(ApiRequester())
    extract_contract = extract.extract()

    transform = TransformData(extract_contract)
    transform_contract = transform.transform()

    load = LoadData(transform_contract)
    load.export()

    logging.info("Pipeline finalizada com sucesso.")
    logging.info(f"Relatório e gráfico salvos em: reports")

if __name__ == "__main__":
    main()