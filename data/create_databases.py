from IMDB_Actors.data import db_helper as con
from IMDB_Actors.data import queries
from IMDB_Actors.data.db_helper import execute_query

#create database schema
#connection = con.create_connection(host_name, user_name, user_password)
#execute_query(connection, queries.create_database_schema_query)
connection = con.create_connection_to_scheme("localhost", "anna", "1234", "imdb")

#drop all tables
#execute_query(connection, queries.drop_all_tables)



#create databases
execute_query(connection, queries.create_actors_query)
execute_query(connection, queries.create_awards_query)
execute_query(connection, queries.create_movies_query)
execute_query(connection, queries.create_actors_in_movies_query)
execute_query(connection, queries.create_actors_have_awards_query)
execute_query(connection, queries.create_genres)
