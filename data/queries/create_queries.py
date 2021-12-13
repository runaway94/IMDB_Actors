# cerate schema
create_database_schema_query = "CREATE DATABASE IF NOT EXISTS imdb"

# cerate databases
create_actors_query = """
     CREATE TABLE actors (
          actorID VARCHAR(50) PRIMARY KEY,
          name TEXT NOT NULL,
          birthdate DATE,
          image TEXT,
          bio TEXT,
          gender ENUM('male', 'female')
    );
    """

create_awards_query = """
    CREATE TABLE awards (
        awardID INTEGER PRIMARY KEY AUTO_INCREMENT,
        year INTEGER,
        category VARCHAR(250),   
        title TEXT
    );
    """

create_actors_have_awards_query = """
    CREATE TABLE actors_have_awards (
        actorID VARCHAR(50),
        awardID INTEGER,
        outcome ENUM('Winner', 'Nominee'),
        description VARCHAR(500),        
        PRIMARY KEY (awardID, actorID, description),
        FOREIGN KEY (awardID) REFERENCES awards(awardID) ON DELETE CASCADE,
        FOREIGN KEY (actorID) REFERENCES actors(actorID) ON DELETE CASCADE
    );
"""

create_movies_query = """
    CREATE TABLE movies (
        movieID VARCHAR(50) PRIMARY KEY,
        title TEXT,
        year INTEGER,
        runtime INTEGER,
        rating DECIMAL(3, 2)
    );
    """

create_genres = """
    CREATE TABLE genres (
        title TEXT,
        movieId VARCHAR(50)
    );
"""

create_actors_in_movies_query = """
    CREATE TABLE  actors_in_movies (
        actorID  VARCHAR(50) NOT NULL,
        movieID VARCHAR(50) NOT NULL,
        CONSTRAINT id PRIMARY KEY (actorID, movieID),
        FOREIGN KEY (movieID) REFERENCES movies(movieID) ON DELETE CASCADE,
        FOREIGN KEY (actorID) REFERENCES actors(actorID) ON DELETE CASCADE
    );
"""

# drop tables
drop_all_tables = """
    DROP TABLE IF EXISTS 
    actors_in_movies, 
    actors_have_awards, 
    awards, 
    actors, 
    movies,
    genres;
"""
