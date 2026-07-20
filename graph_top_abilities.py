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
        abilities.name,
        COUNT(*) AS pokemon_count
    FROM pokemon_abilities
    JOIN abilities ON pokemon_abilities.ability_id = abilities.id
    GROUP BY abilities.id
    ORDER BY pokemon_count DESC,
        abilities.name ASC
    LIMIT 30;"""
df = pd.read_sql(query, engine)

sns.barplot(data=df, x='pokemon_count', y='name')
plt.title('Top 30 Most Common Pokemon Abilities')
plt.show()
