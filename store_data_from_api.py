import constants
import requests

from models.base import Base
from models.ability import Ability
from models.pokemon import Pokemon
from models.pokemon_ability import PokemonAbility

from pprint import pprint

from sqlalchemy import create_engine, select, delete, text
from sqlalchemy.orm import Session

engine = create_engine(
        f"mysql+mysqlconnector://{constants.DB_USERNAME}:{constants.DB_PASSWORD}@{constants.DB_HOST}:{constants.DB_PORT}/{constants.DB_NAME}",
        echo=True)

Base.metadata.create_all(engine)

def retrieve_json_from_url(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error fetching data calling {url}: {response.status_code}")
            return {}

    except requests.exceptions.RequestException as e:
        print(f"An error occurred calling {url}: {e}")
        return {}


def store_abilities(abilities, abilities_map, engine):
    with Session(engine) as session:
        for result in abilities['results']:
            url = result['url']
            ability = retrieve_json_from_url(url)

            if ability != {}:
                api_id = ability['id']
                name = ability['name']
                record_id = None
                existing_record = session.query(Ability).filter_by(api_id=api_id).first()

                if existing_record:
                    existing_record.name = name
                    existing_record.url = url
                    record_id = existing_record.id
                else:
                    new_ability = Ability(api_id, name, url)
                    session.add(new_ability)
                    session.flush()
                    record_id = new_ability.id

                print(f"=====> storing Ability: api_id {api_id}, name {name}, url {url}")
                session.commit()
                abilities_map[url] = record_id

        if abilities['next']:
            store_abilities(retrieve_json_from_url(abilities['next']), abilities_map, engine)

def store_pokemon_abilities(pokemon_id, abilities, abilities_map, engine):
    with Session(engine) as session:
        # delete pokemon's old pokemon_abilities in case outdated
        query = text("DELETE FROM pokemon_abilities WHERE pokemon_id = :pokemon_id")
        session.execute(query, {'pokemon_id': pokemon_id})

        for ability in abilities:
            ability_id = abilities_map[ability['ability']['url']]
            if ability_id:
                # save pokemon's new pokemon_abilities
                session.add(PokemonAbility(pokemon_id, ability_id))
            session.commit()

def store_pokemons(pokemons, abilities_map, engine):
    with Session(engine) as session:
        for result in pokemons['results']:
            url = result['url']
            pokemon = retrieve_json_from_url(url)
            if pokemon != {}:
                api_id = pokemon['id']
                name = pokemon['name']
                position = pokemon['order']
                record_id = None
                existing_record = session.query(Pokemon).filter_by(api_id=api_id).first()

                if existing_record:
                    existing_record.name = name
                    existing_record.position = position
                    existing_record.url = url
                    record_id = existing_record.id
                else:
                    new_pokemon = Pokemon(api_id, name, position, url)
                    session.add(new_pokemon)
                    session.flush()
                    record_id = new_pokemon.id

                print(f"-----> storing Pokemon: api_id {api_id}, name {name}, position {position}, url {url}")
                session.commit()
                store_pokemon_abilities(record_id, pokemon['abilities'], abilities_map, engine)

        if pokemons['next']:
            store_pokemons(retrieve_json_from_url(pokemons['next']), abilities_map, engine)


abilities_map = {}
store_abilities(retrieve_json_from_url(constants.API_ABILITY_URL), abilities_map, engine)
store_pokemons(retrieve_json_from_url(constants.API_POKEMON_URL), abilities_map, engine)
