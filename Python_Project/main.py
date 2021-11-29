from sqllite_test import test
import mySqlTest
# This is a sample Python script.

# Press Umschalt+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Strg+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    #test()
    #connection = mySqlTest.test()
    connection = mySqlTest.create_connection("localhost", "anna", "1234", "actors")
    mySqlTest.print_all_databeses("localhost", "anna", "1234")
    create_users_table = """
    CREATE TABLE IF NOT EXISTS users (
      id INTEGER PRIMARY KEY,
      name TEXT NOT NULL,
      age INTEGER,
      gender TEXT,
      nationality TEXT
    );
    """
    mySqlTest.execute_query(connection, create_users_table)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
