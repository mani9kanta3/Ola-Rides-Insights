import os
import pandas as pd
from sqlalchemy import create_engine

def get_engine():
    db_url = os.environ.get("DATABASE_URL")
    if not db_url:
        raise ValueError("DATABASE_URL environment variable not set")

    return create_engine(db_url)

def run_query(query):
    engine = get_engine()
    return pd.read_sql(query, engine)
