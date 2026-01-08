import pandas as pd
from sqlalchemy import create_engine

def get_engine():
    engine = create_engine(
        "postgresql+psycopg2://postgres:Manikanta%403@localhost:5432/ola_analytics"
    )
    return engine

def run_query(query):
    engine = get_engine()
    return pd.read_sql(query, engine)