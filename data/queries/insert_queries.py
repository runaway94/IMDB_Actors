"""insert_queries.py
--------
stores all insert queries

"""
def insert_into_query(database, key_value_pairs):
    """
    creates query to insert values into one table
    :type database: str
    :param database: name of database to insert in
    :type key_value_pairs: dict
    :param key_value_pairs: keys where to insert, values what should be inserted
    :returns: insert into query
    :rtype: str
    """
    query = "INSERT IGNORE INTO imdb.{database_name} ({keys}) VALUES ({values});"

    keys = ""
    for key in key_value_pairs.keys():
        keys = keys + key + ", "
    keys = keys[:len(keys) - 2]

    values = ""
    for value in key_value_pairs.values():
        values = values + str(value) + ", "
    values = values[:len(values) - 2]

    return query.format(database_name=database, keys=keys, values=values)
