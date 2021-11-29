import mysql.connector
from mysql.connector import Error


def create_connection(host_name, user_name, user_password):
    connection = None

    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password
        )
        print("Connection to MySQL DB successful")

    except Error as e:
        print(f"The error '{e}' occurred")

    return connection


def create_database(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        print("Database created successfully")
    except Error as e:
        print(f"The error '{e}' occurred")


def create_connection(host_name, user_name, user_password, db_name):
    connection = None

    try:

        connection = mysql.connector.connect(

            host=host_name,
            user=user_name,
            passwd=user_password,
            database=db_name

        )

        print("Connection to MYSQL DB successful")

    except Error as e:

        print(f"The error '{e}' occurred")

    return connection


def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query executed successfully")
    except Error as e:
        print(f"The error '{e}' occurred")

def print_all_databeses(host_name, user_name, user_password):
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password
        )

        mycursor = connection.cursor()

        mycursor.execute("SHOW DATABASES")

        for x in mycursor:
            print(x)

    except Error as e:
        print(f"The error '{e}' occurred")

    return connection

def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query executed successfully")
    except Error as e:
        print(f"The error '{e}' occurred")