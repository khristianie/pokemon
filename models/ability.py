import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)

if project_root not in sys.path:
    sys.path.insert(0, project_root)

from models.base import Base

from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship

class Ability(Base):
    __tablename__ = 'abilities'
    id = Column(Integer, primary_key=True)
    api_id = Column(Integer)
    name = Column(String(length=100))
    url = Column(String(length=2048))

    pokemon_abilities = relationship('PokemonAbility', back_populates='ability')

    def __init__(self, api_id, name, url=None):
        self.api_id = api_id
        self.name = name
        self.url = url

    def __repr__(self):
        return f"<Ability[{self.id}]({self.api_id}) -> {self.name} -> {self.url}]>"
