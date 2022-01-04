import json

config_path = "data/db_config.json"
config_path = "db_config.json"


def init_config(host, user, password, database):
    """
    Initializes the connection configuration for the database
    """
    config = {"host": host, "user": user, "password": password, "database": database}
    with open(config_path, 'w') as f:
        json.dump(config, f)


def update_config(key, value):
    with open(config_path, 'r') as f:
        config = json.load(f)

    # edit the data
    config[key] = value

    # write it back to the file
    with open(config_path, 'w') as f:
        json.dump(config, f)


def get_config():
    with open(config_path, 'r') as f:
        config = json.load(f)
    return config


init_config("localhost", "anna", "1234", "imdb")
