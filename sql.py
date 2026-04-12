import sqlite3
import pandas as pd
import os

DB_PATH = os.path.join(os.getcwd(), "data.db")


def run_query(query):
    try:
        if not query.strip().upper().startswith("SELECT"):
            return "Error: Only SELECT queries are allowed"

        conn = sqlite3.connect(DB_PATH)
        df = pd.read_sql_query(query, conn)
        conn.close()

        return df

    except Exception as e:
        return str(e)
