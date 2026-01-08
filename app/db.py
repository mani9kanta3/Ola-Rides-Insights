import os
import pandas as pd
from sqlalchemy import create_engine

DATABASE_URL = os.environ["DATABASE_URL"]

engine = create_engine(DATABASE_URL)

def run_query(query):
    return pd.read_sql(query, engine)
