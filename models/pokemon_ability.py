import os
import pandas as pd
import sys

from pprint import pprint

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)

if project_root not in sys.path:
    sys.path.insert(0, project_root)

from models.base import Base

from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

class PokemonAbility(Base):
    __tablename__ = 'pokemon_abilities'
    query_chunk = 50

    pokemon_id = Column(Integer, ForeignKey('pokemons.id'), primary_key=True)
    ability_id = Column(Integer, ForeignKey('abilities.id'), primary_key=True)

    pokemon = relationship('Pokemon', back_populates='pokemon_abilities')
    ability = relationship('Ability', back_populates='pokemon_abilities')

    def __init__(self, pokemon_id, ability_id):
        self.pokemon_id = pokemon_id
        self.ability_id = ability_id

    def __repr__(self):
        return f"<PokemonAbility[({self.pokemon_id}) {self.pokemon.name} -> ({self.ability_id}) {self.ability.name}]>"

    @classmethod

    def display_table_data(cls, engine):
        print('========== POKEMON_ABILITIES ==========')
        counter = 0
        query = 'SELECT * FROM pokemon_abilities ORDER BY pokemon_id, ability_id'
        for chunk in pd.read_sql_query(query, con=engine, chunksize=cls.query_chunk):
            print(f"-- from {counter}... for POKEMON_ABILITIES")
            pprint(chunk)
            counter += cls.query_chunk
        print('========== POKEMON_ABILITIES ==========')
