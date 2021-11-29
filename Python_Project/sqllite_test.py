import sqlite3

from sqlite3 import Error


def create_connection(path):

    connection = None

    try:
        connection = sqlite3.connect(path)
        print("Connection to SQLite DB successful")

    except Error as e:
        print(f"The error '{e}' occurred")

    return connection

def test():
    connection = create_connection("Actors.sqlite")
    create_database_schema_query = "CREATE DATABASE my_app"
    create_database(connection, create_database_schema_query)

def create_database(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        print("Database created successfully")
    except Error as e:
        print(f"The error '{e}' occurred")
