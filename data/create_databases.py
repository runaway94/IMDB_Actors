from IMDB_Actors.data import db_helper as con
from IMDB_Actors.data.db_connection import Connection
from IMDB_Actors.data.db_helper import execute_query
from IMDB_Actors.data.queries import create_queries

# #create database schema
# connection = con.create_connection("localhost", "anna", "1234")
# execute_query(connection, create_queries.create_database_schema_query)
#
# connection = con.create_connection_to_scheme("localhost", "anna", "1234", "imdb")
#
# #drop all tables
# execute_query(connection, create_queries.drop_all_tables)
#
# #create databases
# execute_query(connection, create_queries.create_actors_query)
# execute_query(connection, create_queries.create_awards_query)
# execute_query(connection, create_queries.create_movies_query)
# execute_query(connection, create_queries.create_actors_in_movies_query)
# execute_query(connection, create_queries.create_actors_have_awards_query)
# execute_query(connection, create_queries.create_genres)

con = Connection()
con.init_data_base()