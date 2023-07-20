from sqlalchemy import create_engine
import pandas as pd
from langchain import SQLDatabase

def load_data(journey_pricing, flights):
    engine = create_engine('sqlite:///:memory:')

    # Write the data to the SQLite database
    flights.to_sql('flights', engine, if_exists='replace', index=False)
    journey_pricing.to_sql('journey_pricing', engine, if_exists='replace', index=False)
    # Check if the data was loaded correctly
    df_loaded = pd.read_sql('SELECT * FROM flights', engine)
    db = SQLDatabase(engine)
    return db