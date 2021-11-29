# cerate schema
create_database_schema_query = "CREATE DATABASE imdb"

# cerate databases
create_actors_query = """
    CREATE TABLE IF NOT EXISTS actors (
      actorID VARCHAR(50) PRIMARY KEY,
      name TEXT NOT NULL,
      birthdate TEXT ,
      image TEXT,
      bio TEXT,
      pos INTEGER 
    );
    """

create_awards_query = """
    CREATE TABLE IF NOT EXISTS awards (
        awardID INTEGER PRIMARY KEY AUTO_INCREMENT,
        year INTEGER,
        category VARCHAR(250),   
        title TEXT
    );
    """

create_actors_have_awards_query = """
    CREATE TABLE IF NOT EXISTS actors_have_awards (
        actorID VARCHAR(50),
        awardID INTEGER,
        outcome TEXT,
        description TEXT,        
        PRIMARY KEY (awardID, actorID),
        FOREIGN KEY (awardID) REFERENCES awards(awardID),
        FOREIGN KEY (actorID) REFERENCES actors(actorID)
    );
"""

create_movies_query = """
    CREATE TABLE IF NOT EXISTS movies (
        movieID VARCHAR(50) PRIMARY KEY,
        title TEXT,
        year INTEGER,
        runtime INTEGER,
        rating DECIMAL(3, 2)
    );
    """

create_genres = """
    CREATE TABLE IF NOT EXISTS genres (
        title TEXT,
        movieId VARCHAR(50)
    );
"""

create_actors_in_movies_query = """
    CREATE TABLE IF NOT EXISTS actors_in_movies (
        actorID  VARCHAR(50) NOT NULL,
        movieID VARCHAR(50) NOT NULL,
        CONSTRAINT id PRIMARY KEY (actorID, movieID),
        FOREIGN KEY (movieID) REFERENCES movies(movieID),
        FOREIGN KEY (actorID) REFERENCES actors(actorID)
    );
"""

#drop tables
drop_all_tables =  """
    drop table imdb.actors_in_movies;
    drop table imdb.actors_have_awards;
    drop table imdb.awards;
    drop table imdb.actors;
    drop table imdb.movies;
"""

# insert into database
def insert_into_query(database, key_value_pairs):
    query = "INSERT INTO imdb.{database_name} ({keys}) VALUES ({values});"

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