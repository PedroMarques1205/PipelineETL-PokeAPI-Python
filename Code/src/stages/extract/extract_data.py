from src.drivers.data_collector import DataCollector
from src.drivers.interfaces.api_requester import ApiRequesterInterface

class ExtractData:

    def __init__(self, api_requester: ApiRequesterInterface) -> None:
        self.__api_requester = api_requester


    def extract(self):
        pokemon_data = self.__api_requester.request_pokemon_details()
        data_frame = DataCollector(pokemon_data).build_dataframe()

        return data_frame