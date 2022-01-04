import csv
import json

import mysql.connector
from mysql.connector import Error

class  Data_Src():
    def __init__(self, host_name, user_name, user_password):
        self.host_name = host_name
        self.user_name = user_name
        self.user_password = user_password

def create_connection(host_name, user_name, user_password):
    con_data = load_connection()
    connection = None

    try:
        connection = mysql.connector.connect(
            host=con_data[0],
            user=con_data[1],
            passwd=con_data[2]
        )

    except Error as e:
        print(f"The error '{e}' occurred")

    return connection



def create_connection_to_scheme(host_name, user_name, user_password, schema):
    connection = None

    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database=schema
        )

    except Error as e:
        print(f"The error '{e}' occurred")

    return connection


def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
    except Error as e:
        print(query + " did not work.")
        print(f"The error '{e}' occurred")


def execute_read_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as e:
        print(query + " did not work.")
        print(f"The error '{e}' occurred")


def execute_read_query_dict(connection, query):
    cursor = connection.cursor(dictionary=True)
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as e:
        print(query + " did not work.")
        print(f"The error '{e}' occurred")


def save_new_connection(host_name, user_name, user_password, database_name):
    try:
        mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
        )

    except Error as e:
        print(f"Looks like something went wrong.\n"
              f"Please check hostname, username and password.\n"
              f"The error '{e}' occurred")
        return False

    csv_file = open("mysql_con.csv", 'w+')
    #TODO save pw crypted
    writer = csv.writer(csv_file, delimiter=",", quotechar=' ')
    writer.writerow([host_name, user_name, user_password, database_name])
    csv_file.close()

    return True


def load_connection():
    csv_file = open("mysql_con.csv", 'r')
    reader = csv.reader(csv_file)
    if reader.line_num != 0:
        raise Exception('You need to define a connection first.')
        return

    return next(reader)


def connection_possible():
    csv_file = open("mysql_con.csv", 'r')
    reader = csv.reader(csv_file)
    if reader.line_num != 0:
        return False
    con = create_connection()
    if con is None:
        return False
    return True

def write_config():
    # with open('config.json', 'r') as f:
    #     config = json.load(f)

    config = {"key1": "value1", "key2": "value2"}

    with open('db_config.json', 'w') as f:
        json.dump(config, f)

    # edit the data
    #config['key3'] = 'value3'

    # write it back to the file
    #with open('config.json', 'w') as f:
        #json.dump(config, f)

#save_new_connection("localhost", "anna", "1234", "imdb")
#print(create_connection("localhost", "anna", "1234"))
#connection_possible()
write_config()