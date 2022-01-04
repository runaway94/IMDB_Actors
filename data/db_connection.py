import mysql

from IMDB_Actors.data.db_config import get_config
from mysql.connector import Error

from IMDB_Actors.data.queries import insert_queries


class Connection:
    table_pk_pairs = {

    }

    def __init__(self):
        config = get_config()
        self.host = config["host"]
        self.user = config["user"]
        self.password = config["password"]
        self.database = config["database"]

    def create_connection(self):
        connection = None

        try:
            connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                passwd=self.password
            )

        except Error as e:
            print(f"The error '{e}' occurred")

        return connection

    def create_connection_to_database(self):
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

        return connection

    def execute_query(self, query):
        connection = self.create_connection_to_database()
        cursor = connection.cursor()
        try:
            cursor.execute(query)
            connection.commit()
        except Error as e:
            print(query + " did not work.")
            print(f"The error '{e}' occurred")

    def execute_read_query_dict(self, query):
        connection = self.create_connection_to_database()
        cursor = connection.cursor(dictionary=True)
        result = None
        try:
            cursor.execute(query)
            result = cursor.fetchall()
            return result
        except Error as e:
            print(query + " did not work.")
            print(f"The error '{e}' occurred")

    def save_value(self, value, table, pk=None):
        if pk is None or not self.exists(table, pk):
            query = insert_queries.insert_into_query(table, value)
            self.execute_query(query)
            return True
        return False

    def exists(self, table, pk):
        pk_name = self.get_primary_key_name(table)
        query = f"SELECT 1 FROM {table} WHERE {pk_name} = {pk};"
        reply = self.execute_read_query_dict(query)
        if len(reply) == 0:
            return False
        return True

    def get_primary_key_name(self, table):
        query = f"""
            SELECT k.column_name
            FROM information_schema.table_constraints t
            JOIN information_schema.key_column_usage k
            USING(constraint_name,table_schema,table_name)
            WHERE t.constraint_type='PRIMARY KEY'
            AND t.table_name='{table}';
        """
        reply = self.execute_read_query_dict(query)
        if len(reply) == 1:
            return reply[0]["COLUMN_NAME"]
        return None
