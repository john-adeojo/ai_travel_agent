from sqlalchemy import create_engine
import pandas as pd
from langchain import SQLDatabase

def load_data(df_flights):
    engine = create_engine('sqlite:///:memory:')

    # Write the data to the SQLite database
    df_flights.to_sql('flights', engine, if_exists='replace', index=False)
    # Check if the data was loaded correctly
    df_loaded = pd.read_sql('SELECT * FROM flights', engine)
    db = SQLDatabase(engine)
    return db