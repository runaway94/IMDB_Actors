SET SQL_SAFE_UPDATES = 0;
DELETE FROM imdb.actors_in_movies;
DELETE FROM imdb.actors_have_awards;
DELETE FROM imdb.genres;
DELETE FROM imdb.movies;
DELETE FROM imdb.actors;
DELETE FROM imdb.awards;
SET SQL_SAFE_UPDATES = 1;