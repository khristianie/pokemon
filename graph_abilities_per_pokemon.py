import constants
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sqlalchemy import create_engine

engine = create_engine(
        f"mysql+mysqlconnector://{constants.DB_USERNAME}:{constants.DB_PASSWORD}@{constants.DB_HOST}:{constants.DB_PORT}/{constants.DB_NAME}",
        echo=True)

query = """
    SELECT
        pokemons.name,
        COUNT(*) AS ability_count
    FROM pokemons
    JOIN pokemon_abilities
        ON pokemons.id = pokemon_abilities.pokemon_id
    GROUP BY pokemons.id;"""
df = pd.read_sql(query, engine)

sns.histplot(df['ability_count'])
plt.title('Number of Abilities per Pokemon')
plt.xlabel('')
plt.ylabel('number of Pokemons')
plt.show()
