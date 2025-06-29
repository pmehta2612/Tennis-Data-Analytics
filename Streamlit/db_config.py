import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="abc%d_@1234_ef",
        database="tennis_db"
    )
