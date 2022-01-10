"""db_connection.py
--------
"""
import mysql
from mysql.connector import Error

from IMDB_Actors.data.db_config import get_config
from IMDB_Actors.data.queries import insert_queries, create_queries
from IMDB_Actors.data.queries.select_queries import select_database_query, primary_key_query


class Connection:
    """Connection to the database"""

    def __init__(self):
        """"loads configuration

        :raises: FileNotFoundError
         """
        try:
            config = get_config()
            self.host = config["host"]
            self.user = config["user"]
            self.password = config["password"]
            self.database = config["database"]
        except FileNotFoundError:
            raise

    def create_connection(self):
        """"creates a connection

        :returns: connection to database
        :rtype: MySQLConnection
        :raises: ConnectionError
        """
        connection = None

        try:
            connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                passwd=self.password
            )

        except Error as e:
            print(f"The error '{e}' occurred. Please check your database configuration.")
            raise ConnectionError

        return connection

    def database_exists(self):
        """"checks if configured database exists

        :returns: connection to database
        :rtype: MySQLConnection
        :raises: ConnectionError
        """
        response = self.execute_read_query(select_database_query.format(db_name=self.database),
                                           connect_to_database=False)
        return len(response) != 0

    def create_connection_to_database(self):
        """"creates a connection to the database

        :returns: connection to database
        :rtype: MySQLConnection
        :raises: ConnectionError
        """
        connection = None

        try:
            connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                passwd=self.password,
                database=self.database
            )

        except Error as e:
            print(f"The error '{e}' occurred")
            raise ConnectionError

        return connection

    def execute_query(self, query, connect_to_database=True):
        """executes query

        :param query: query to be executed
        :type query: str
        :param connect_to_database: connect to specific database if True (True by default)
        :type connect_to_database: bool
        """
        if connect_to_database:
            connection = self.create_connection_to_database()
        else:
            connection = self.create_connection()
        cursor = connection.cursor()
        try:
            cursor.execute(query)
            connection.commit()
        except Error as e:
            print(query + " did not work.")
            print(f"The error '{e}' occurred")

    def execute_read_query(self, query, dict_res=True, connect_to_database=True):
        """executes query with return value

        :param query: query to be executed
        :type query: str
        :param connect_to_database: connect to specific database if True (True by default)
        :type connect_to_database: bool
        :param dict_res: returns values as dictionary (True by default)
        :type dict_res: bool
        :returns: result of query
        :rtype: list or dict
        """
        if connect_to_database:
            connection = self.create_connection_to_database()
        else:
            connection = self.create_connection()
        cursor = connection.cursor(dictionary=dict_res)
        result = None
        try:
            cursor.execute(query)
            result = cursor.fetchall()
            return result
        except Error as e:
            print(query + " did not work.")
            print(f"The error '{e}' occurred")

    def save_value(self, value, table, pk=None):
        """saves new value in table

        :param value: new values to save
        :param table: table in which table the values should be stored
        :type table: str
        :param pk: pk optional, to check if value already exists
        :type pk: str
        :returns: True if insert was successful
        :rtype: bool
        """
        if pk is None or not self.entry_exists(table, pk):
            query = insert_queries.insert_into_query(table, value)
            self.execute_query(query)
            return True
        return False

    def entry_exists(self, table, pk):
        """ Checks if entry already exists

        :param table: table to check
        :type table: str
        :param pk: primary key
        :type pk: str
        :returns: True if value already exists in db
        :rtype: bool
        """
        pk_name = self.get_primary_key_name(table)
        query = f"SELECT 1 FROM {table} WHERE {pk_name} = {pk};"
        reply = self.execute_read_query(query)
        if len(reply) == 0:
            return False
        return True

    def get_primary_key_name(self, table):
        """ primary key of the table

        :param table: table to check
        :type table: str
        :returns: primary key
        :rtype: str
        """
        reply = self.execute_read_query(primary_key_query.format(table_name=table))
        if len(reply) != 0:
            return reply[0]["COLUMN_NAME"]
        return None

    def init_data_base(self):
        """ initializes database it it does not exist, drops and creates all tables
        """

        # create database schema
        self.execute_query(create_queries.create_database_schema_query.format(db_name=self.database), False)

        # drop all tables
        self.execute_query(create_queries.drop_all_tables)

        # create databases
        self.execute_query(create_queries.create_actors_query)
        self.execute_query(create_queries.create_awards_query)
        self.execute_query(create_queries.create_movies_query)
        self.execute_query(create_queries.create_actors_in_movies_query)
        self.execute_query(create_queries.create_actors_have_awards_query)
        self.execute_query(create_queries.create_genres)
