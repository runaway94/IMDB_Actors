# insert into database
def insert_into_query(database, key_value_pairs):
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


def is_award_in_database(award_category, award_year):
    query = "SELECT COUNT(*) FROM imdb.awards WHERE category = {category} AND year = {year};".format(
        category=award_category, year=award_year)
    return query

def is_movie_in_database(movie_id):
    query = "SELECT COUNT(*) FROM imdb.movies WHERE movieID = {id};".format(
        id=movie_id)
    return query

def get_id_from_award(award_category, award_year, award_title):
    query = "SELECT awardID FROM imdb.awards WHERE category = {category} AND year = {year} AND title = {title};".format(
        category=award_category, year=award_year, title = award_title)
    return query