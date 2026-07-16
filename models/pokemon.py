import os
import sys

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

    pokemon_abilities = relationship('PokemonAbility', back_populates='pokemon')

    def __init__(self, api_id, name, position=None, url=None):
        self.api_id = api_id
        self.name = name
        self.position = position
        self.url = url

    def __repr__(self):
        return f"<Pokemon[{self.id}]({self.api_id}) -> {self.name} -> {self.position} -> {self.url}]>"
