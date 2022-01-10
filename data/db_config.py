"""db_config.py
--------
module that saves, updates and reads the database configuration
"""
import json

from IMDB_Actors.constants import db_config

config_path = db_config


def init_config(host, user, password, database):
    """ Initializes the connection configuration for the database

    :param host: Host name for the database connection
    :type host: str
    :param user:  User name for the database connection
    :type user: str
    :param password: Password for the database connection
    :type password: str
    :param database: Name of the database
    :type database: str
    """
    config = {"host": host, "user": user, "password": password, "database": database}
    with open(config_path, 'w') as f:
        json.dump(config, f)


def update_config(key, value):
    """Updates database configuration

    :type key: str
    :param key: key of the value that should be changed
    :type value: str
    :param value: new value
    :raises: FileNotFoundError
    """
    with open(config_path, 'r') as f:
        config = json.load(f)

    # edit the data
    config[key] = value

    # write it back to the file
    with open(config_path, 'w') as f:
        json.dump(config, f)


def get_config():
    """Reads the configuration of the database connection.

    :returns: the database configuration
    :rtype: dict
    :raises: FileNotFoundError
    """
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
            return config
    except FileNotFoundError:
        print("There is no database configuration yet.")
        raise


