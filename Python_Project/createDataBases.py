import mysql.connector
from mysql.connector import Error

create_database_schema_query = "CREATE DATABASE imdb"

create_actors_query = """
    CREATE TABLE IF NOT EXISTS actors (
      actorID INTEGER PRIMARY KEY AUTO_INCREMENT,
      name TEXT NOT NULL,
      age INTEGER,
      gender TEXT,
      nationality TEXT,
      bio TEXT
    );
    """

create_awards_query = """
    CREATE TABLE IF NOT EXISTS awards (
        awardID INTEGER PRIMARY KEY AUTO_INCREMENT,
        FOREIGN KEY (actorID) REFERENCES actors(actorID),
        category TEXT,
        outcome ENUM('winner', 'nominated'),
        year INTEGER
    );
    """

create_movies_query = """
    CREATE TABLE IF NOT EXISTS movies (
        movieID INTEGER PRIMARY KEY AUTO_INCREMENT,
        title TEXT,
        year INTEGER,
        runtime INTEGER,
        genre TEXT,
        rating DECIMAL(3, 2)
    );
    """

create_actors_in_movies_query = """
    CREATE TABLE IF NOT EXISTS actors_in_movies (
        actorID INTEGER NOT NULL,
        movieID INTEGER NOT NULL,
        CONSTRAINT id PRIMARY KEY (ID, LastName),
        FOREIGN KEY (movieID) REFERENCES movies(movieID),
        FOREIGN KEY (actorID) REFERENCES actors(actorID)
    );
"""