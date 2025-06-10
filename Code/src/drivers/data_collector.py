import pandas as pd
import logging

from typing import List, Dict

logger = logging.getLogger(__name__)

class DataCollector:
    def __init__(self, pokemons_data: List[Dict]):
        self.pokemons_data = pokemons_data

    def build_dataframe(self) -> pd.DataFrame:
        logger.info("Construindo DataFrame com dados dos Pokémons")

        df = pd.DataFrame(self.pokemons_data)

        df['ID'] = df['id']
        df['Nome'] = df['name'].str.title()
        df['Experiência Base'] = df['base_experience']
        df['Tipos'] = df['types'].map(lambda x: [t['type']['name'].title() for t in x])

        def get_stat(stats, stat_name):
            return next((s['base_stat'] for s in stats if s['stat']['name'] == stat_name), None)

        df['HP'] = df['stats'].map(lambda x: get_stat(x, 'hp'))
        df['Ataque'] = df['stats'].map(lambda x: get_stat(x, 'attack'))
        df['Defesa'] = df['stats'].map(lambda x: get_stat(x, 'defense'))

        result_df = df[['ID', 'Nome', 'Experiência Base', 'Tipos', 'HP', 'Ataque', 'Defesa']]
        return result_df

