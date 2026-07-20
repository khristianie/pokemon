import os
import pandas as pd
import sys

from pprint import pprint

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)

if project_root not in sys.path:
    sys.path.insert(0, project_root)

from models.base import Base

from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship

class Pokemon(Base):
    __tablename__ = 'pokemons'

    id = Column(Integer, primary_key=True)
    api_id = Column(Integer)
    name = Column(String(length=100))
    position = Column(Integer)
    url = Column(String(length=2048))
    query_chunk = 50

    pokemon_abilities = relationship('PokemonAbility', back_populates='pokemon')

    def __init__(self, api_id, name, position=None, url=None):
        self.api_id = api_id
        self.name = name
        self.position = position
        self.url = url

    def __repr__(self):
        return f"<Pokemon[{self.id}]({self.api_id}) -> {self.name} -> {self.position} -> {self.url}]>"

    @classmethod

    def display_table_data(cls, engine):
        print('========== POKEMONS ==========')
        counter = 0
        query = 'SELECT * FROM pokemons ORDER BY position, api_id'
        for chunk in pd.read_sql_query(query, con=engine, chunksize=cls.query_chunk):
            print(f"-- from {counter}... for POKEMONS")
            pprint(chunk)
            counter += cls.query_chunk
        print('========== POKEMONS ==========')
