"""IMBd.py
--------
commandline application to control program by user input"""
import threading

from IMDB_Actors.application.scrape.scrape import scrape_data
from IMDB_Actors.data.db_config import init_config, update_config
from IMDB_Actors.data.db_connection import Connection
from IMDB_Actors.presentation.app import app

start_from_scratch_command = "--start"
configure_database_command = "--configure"
help_command = "--help"
scrape_command = "--scrape"
start_web_app_command = "--show"
exit_command = "--exit"

global running
running = True

logo_text = """
  _____ __  __ _____  ____    __  __            _         _____                                
 |_   _|  \/  |  __ \|  _ \  |  \/  |          (_)       / ____|                               
   | | | \  / | |  | | |_) | | \  / | _____   ___  ___  | (___   ___ _ __ __ _ _ __   ___ _ __ 
   | | | |\/| | |  | |  _ <  | |\/| |/ _ \ \ / / |/ _ \  \___ \ / __| '__/ _` | '_ \ / _ \ '__|
  _| |_| |  | | |__| | |_) | | |  | | (_) \ V /| |  __/  ____) | (__| | | (_| | |_) |  __/ |   
 |_____|_|  |_|_____/|____/  |_|  |_|\___/ \_/ |_|\___| |_____/ \___|_|  \__,_| .__/ \___|_|   
                                                                              | |              
                                                                              |_|              
"""


def print_help_text():
    """Shows help and all possible commands
    """
    help_text = f"In this application you can scrape information about the top 50 most popular actors" \
                f" and actresses from a imdb website.\n Afterwards you can analyze the information about each actor, " \
                f"their movies and awards. \n\n" \
                f"     -----------------------COMMANDS-----------------------\n" \
                f"     {start_from_scratch_command}: {start_from_scratch.__doc__} " \
                f"{help_command}: { print_help_text.__doc__} " \
                f"{configure_database_command}: {configure_database.__doc__} " \
                f"{scrape_command}: {scrape_information.__doc__} " \
                f"{start_web_app_command}: {start_web_app.__doc__} " \
                f"{exit_command}: {exit_application.__doc__} " \
                f"------------------------------------------------------\n" \
                f"If you are new to this application you can simply use {start_from_scratch_command} and you will be guided."
    print(help_text)


def start_from_scratch():
    """Starts from scratch. Tells you exactly what you need to do next step by step.
    """
    print("Since this application needs to store information in a mySQL database, you need to configure your database "
          "information first. Please make sure that you have installed mySQL. ")
    if not configure_database():
        return
    if not scrape_information():
        return
    print("Great! Thank you for your patience. Everything we need is stored in your database. So let's start the web "
          "application.")
    start_web_app()


def configure_database():
    """Configure the database connection

    :returns: True if connection to database is possible with new configuration, else False
    :rtype: bool
    """
    print("Please configure your database connection.")
    host_name = input("Host: ")
    user_name = input("User name: ")
    user_password = input("Password: ")
    database_name = input("Name of your database: ")
    init_config(host_name, user_name, user_password, database_name)
    try:
        con = Connection()
        con.create_connection()
    except (FileNotFoundError, ConnectionError):
        return False
    print("Database configuration updated.")
    return True


def create_db(con):
    """Initializes the databases

    :param con: Database Connection
    :type con: Connection
    :returns: True if database was created successfully, False otherwise
    :rtype: bool
    """
    try:
        con.create_connection()
    except ConnectionError:
        print("Connection to database failed. Please check your configurations.")
        return False
    if con.database_exists():
        print(f"The database {con.database} already exists. If you continue, tables and data in your database might "
              f"be lost.\n"
              f"If you want to rename the database type '-rename'. \n"
              f"If you would like to continue anyways type '-continue.")
        if not check_answer('-continue', '-rename'):
            rename_database(con)

    print("Database and tables created successfully.")
    con.init_data_base()
    return True


def rename_database(con):
    """Renames database name in configuration file

    :param con: Database Connection
    :type con: Connection
    """
    new_name = input("Enter new name:")
    update_config("database", new_name)
    print("Rename successful. Starting to create databases...")
    create_db(con)


def scrape_information():
    """Starts scraping the data from the imdb page

    :returns: True if scraping worked with no errors, False otherwise
    :rtype: bool
    """
    try:
        con = Connection()
        create_db(con)
        print("Start scraping information . . .")
        try:
            scrape_data()
        except Exception as e:
            print(f"Some thing went wrong during the scraping: {e}\n"
                  f"Please type '--scrape' to try again.")

    except (FileNotFoundError, ConnectionError):
        print("Connection to database failed. Please check your configurations.")
        return False
    return True


def start_web_app():
    """Starts web application on http://127.0.0.1:5000/
    """
    try:
        con = Connection()
        con.create_connection_to_database()
        web_thread = threading.Thread(target=app.run)
        web_thread.setDaemon(True)
        web_thread.start()
        print("Web application started. Please visit http://127.0.0.1:5000/ in your browser.")

    except (ConnectionError, FileNotFoundError):
        print("Connection to database failed. Please check your configurations.")


def exit_application():
    """Ends the application
    """
    print("Shuting down application...")
    global running
    running = False


def check_answer(yes_answer, no_answer):
    """Evaluates user input

    :param yes_answer: user input if user agrees
    :type yes_answer: str
    :param no_answer: user input if user disagrees
    :type no_answer: str
    :returns: True if user agrees
    :rtype: bool
    """
    answer = input().lower()
    if answer == no_answer:
        return False
    elif answer != yes_answer:
        print(f"invalid argument. Please type '{yes_answer}' to agree or '{no_answer}'.")
        return check_answer(yes_answer, no_answer)
    return True


def switcher_user_input(input):
    """Finds right function for user input

    :param input: user input
    :type input: str
    :returns: corresponding function
    :rtype: function
    """
    switcher = {
        help_command: print_help_text,
        start_from_scratch_command: start_from_scratch,
        configure_database_command: configure_database,
        scrape_command: scrape_information,
        start_web_app_command: start_web_app,
        exit_command: exit_application
    }

    return switcher.get(input, lambda: print(f"Invalid Argument, "
                                             "please chose another one or type {help_command} to show the options."))


if __name__ == '__main__':
    print(logo_text)
    print_help_text()
    while running:
        user_input = input("\nPlease enter your command: ")
        func = switcher_user_input(user_input)
        func()
