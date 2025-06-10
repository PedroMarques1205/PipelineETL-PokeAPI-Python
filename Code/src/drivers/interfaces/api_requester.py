from abc import ABC, abstractmethod
from typing import List, Dict


class ApiRequesterInterface(ABC):

    @staticmethod
    @abstractmethod
    def request_list_init_pokemons() -> List[Dict[str, str]]:
        pass

    @abstractmethod
    def request_pokemon_details(self) -> List[Dict]:
        pass