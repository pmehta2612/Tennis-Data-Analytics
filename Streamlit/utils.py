import pandas as pd
from db_config import get_connection

def run_query(query, params=None):
    conn = get_connection()
    df = pd.read_sql(query, conn, params=params)
    conn.close()
    return df
