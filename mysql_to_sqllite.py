# Exporting MySQL database to SQLlite database
# Import Libraries
import pandas as pd
import sqlite3
import mysql.connector

# MySQL connection
mysql_conn = mysql.connector.connect(
    host="localhost",
    user="root",
    port = "3306",
    password="abc%d_@1234_ef",
    database="tennis_db"
)

# SQLite connection
sqlite_conn = sqlite3.connect("tennis_db.sqlite")

# Tables to export
tables = [
    'categories',
    'competitions',
    'complexes',
    'venues',
    'competitor_rankings',
    'competitors'
]

# Export each table
for table in tables:
    df = pd.read_sql(f"SELECT * FROM {table}", mysql_conn)
    df.to_sql(table, sqlite_conn, if_exists='replace', index=False)
    print(f"{table} exported to SQLite.")

# Close connection
mysql_conn.close()
sqlite_conn.close()
