import constants
import itertools

from models.base import Base
from models.ability import Ability
from models.pokemon import Pokemon
from models.pokemon_ability import PokemonAbility

from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

engine = create_engine(
        f"mysql+mysqlconnector://{constants.DB_USERNAME}:{constants.DB_PASSWORD}@{constants.DB_HOST}:{constants.DB_PORT}/{constants.DB_NAME}",
        echo=False)

Base.metadata.create_all(engine)

with Session(engine) as session:
    pokemons = session.scalars(select(Pokemon)).all()
    chunk_size = 10
    counter = 1

    for chunk in itertools.batched(pokemons, chunk_size):
        for pokemon in chunk:
            pokemon.display(counter)
            counter += 1
        if counter < len(pokemons):
            user_input = input("\nPress any key for next page, or [Q]uit: ").strip().lower()
            if user_input == 'q':
                break
