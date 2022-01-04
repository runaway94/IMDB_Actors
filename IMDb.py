from IMDB_Actors.data.db_connection import Connection

#print(
 #   "Hello, welcome to the IMDb analyses software where you can find interesting information about our favourite actors!\n")


def start():
    from IMDB_Actors.data.db_helper import connection_possible
    if not connection_possible():
        print("Since this software needs to store information to a locale database, please enter the following "
              "information:")
        change_data_src()


def change_data_src():
    host_name = input("Host: ")
    user_name = input("User name: ")
    user_password = input("Password: ")
    database_name = input("And how should the database be called? ")
    from IMDB_Actors.data.db_helper import save_new_connection
    if save_new_connection(host_name, user_name, user_password, database_name):
        print("The connection was successful!")


con = Connection()
print(con.host)
