from IMDB_Actors.data.db_config import init_config
from IMDB_Actors.data.db_connection import Connection



def change_data_src():
    print("Please connect to database.")
    host_name = input("Host: ")
    user_name = input("User name: ")
    user_password = input("Password: ")
    database_name = input("And how should the database be called? ")
    #init_config(host_name, user_name, user_password, database_name)
    init_config("localhost", "anna", "123", "imdb")
    con = Connection()
    #con.create_connection()
    if not con.test_connection():
        print("Connection is not possible. Please check your input and try again.")
        change_data_src()


def print_help_text():
    print("Help text")


def start_web_app():
    pass


def scrape():
    pass


def create_db():
    pass


if __name__ == '__main__':
    print("Hello. Welcome to imdBest, the software that provides you with the best infos about our favourite actors.\n"
          "Please tell me what you'd like to do or type -help for help")
    user_input = input()
    switcher = {
        '-help': print_help_text(),
        '-connect': change_data_src(),
        '-scrape': scrape(),
        '-create': create_db(), 
        '-show': start_web_app()
        
    }
    change_data_src()
