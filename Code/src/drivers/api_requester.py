import requests
import logging

from typing import List, Dict
from concurrent.futures import ThreadPoolExecutor, as_completed
from src.common.constants_utils import BASE_URL
from src.drivers.interfaces.api_requester import ApiRequesterInterface

logger = logging.getLogger(__name__)

class ApiRequester(ApiRequesterInterface):

    @staticmethod
    def request_list_init_pokemons() -> List[Dict[str, str]]:
        url = BASE_URL
        logger.info("Iniciando requisição GET %s", url)
        try:
            response = requests.get(url)
            response.raise_for_status()
        except requests.RequestException as e:
            logger.error("Erro na requisição %s: %s", url, e, exc_info=True)
            raise
        else:
            logger.info(
                "Resposta recebida: status=%s, conteúdo=%r",
                response.status_code,
                response.text[:200]
            )
            return response.json()['results']


    def request_pokemon_details(self) -> List[Dict]:
        logger.info("Iniciando requisição dos detalhes dos pokemons")
        pokemons_list = self.request_list_init_pokemons()
        urls = [pokemon['url'] for pokemon in pokemons_list]
        results = []
        failed_count = 0

        def fetch(url):
            logger.info(f"Iniciando requisição para {url}")
            try:
                resp = requests.get(url)
                resp.raise_for_status()
                logger.debug(f"Requisição para {url} finalizada com status {resp.status_code}")
                return resp.json()
            except requests.RequestException as e:
                logger.error(f"Erro na requisição {url}: {e}", exc_info=True)
                return None

        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = {executor.submit(fetch, url): url for url in urls}
            for future in as_completed(futures):
                data = future.result()
                if data:
                    results.append(data)
                else:
                    failed_count += 1

        logger.info(f"Finalizada a requisição dos detalhes: {len(results)} sucessos, {failed_count} falhas")
        return results