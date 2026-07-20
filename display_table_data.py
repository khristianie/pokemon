import constants

from models.ability import Ability
from models.pokemon import Pokemon
from models.pokemon_ability import PokemonAbility

from sqlalchemy import create_engine

engine = create_engine(
        f"mysql+mysqlconnector://{constants.DB_USERNAME}:{constants.DB_PASSWORD}@{constants.DB_HOST}:{constants.DB_PORT}/{constants.DB_NAME}",
        echo=True)

Pokemon.display_table_data(engine)
Ability.display_table_data(engine)
PokemonAbility.display_table_data(engine)
