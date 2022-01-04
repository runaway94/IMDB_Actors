from imagecodecs import none_check
from wordcloud import WordCloud

from IMDB_Actors.data import db_helper as con, db_helper
from IMDB_Actors.data.queries.select_queries import *
import matplotlib.pyplot as plt
from collections import Counter


def get_actor_for_table():
    connection = con.create_connection_to_scheme("localhost", "anna", "1234", "imdb")
    actor_reply = db_helper.execute_read_query(connection, get_auctors_query)
    actors = []
    pos = 0
    for row in actor_reply:
        id = row[0]
        pos = pos + 1
        best_movie = get_most_popular_movie(id, connection)
        new_movie = get_newest_movie(id, connection)
        actor = {
            'id': row[0],
            'pos': pos,
            'name': row[1],
            'birth': row[2],
            'amount_movies': row[4],
            'rating_avg': str(row[3])[:3],
            'pop_movie': best_movie,
            'new_movie': new_movie,
        }
        actors.append(actor)
    return actors


def get_most_popular_movie(id, connection):
    best_mov_qu = get_best_rated_movie(id)
    best_rated_mov_repl = db_helper.execute_read_query(connection, best_mov_qu)
    title = best_rated_mov_repl[0][0]
    rating = best_rated_mov_repl[0][1]
    return title + " (" + str(rating)[:3] + ")"


def get_newest_movie(id, connection):
    new_mov_qu = get_newest_movie_query(id)
    new_mov_repl = db_helper.execute_read_query(connection, new_mov_qu)
    title = new_mov_repl[0][0]
    year = new_mov_repl[0][1]
    return title + " (" + str(year) + ")"


def get_movie_amount(id, connection):
    query = "select count(*) from actors_in_movies where actorID = '{id}'; ".format(id=id)
    repl = db_helper.execute_read_query(connection, query)
    return repl[0][0]


def get_actor_rating(id, connection):
    query = "select avg(rating) from actors_in_movies join movies on actors_in_movies.movieID = movies.movieID where actors_in_movies.actorID = '{id}';".format(
        id=id)
    repl = db_helper.execute_read_query(connection, query)
    return repl[0][0]


def get_top_genre(id, connection):
    query = "select count(*) as amount, title from actors_in_movies join genres on genres.movieId = actors_in_movies.movieID where actors_in_movies.actorID = '{id}' group by title order by amount desc limit 1;".format(
        id=id)
    repl = db_helper.execute_read_query(connection, query)
    genre = str(repl[0][1]) + " (" + str(repl[0][0]) + ")"
    return genre


def get_single_actor(id):
    query = get_actor_information_query(id)
    connection = con.create_connection_to_scheme("localhost", "anna", "1234", "imdb")
    actor_reply = db_helper.execute_read_query(connection, query)
    row = actor_reply[0]
    award_info = get_award_info_of_user(id, connection)
    new_movie = get_newest_movie(id, connection)
    top_movie = get_most_popular_movie(id, connection)
    s = top_movie.index('(') + 1
    top_rating = top_movie[s:-1]
    movies = get_movie_amount(id, connection)
    actor_rating = get_actor_rating(id, connection)
    actor_rating = round(actor_rating, 2)

    actor = {
        'id': row[0],
        'name': row[1],
        'birth': row[2],
        'image': row[3],
        'bio': row[4],
        'gender': row[5],
        'amount_awards': award_info['amount_awards'],
        'amount_wins': award_info['amount_wins'],
        'last_award': award_info['last_award'],
        'new_movie': new_movie,
        'top_movie': top_movie,
        'movies': movies,
        'top_rating': top_rating,
        'rating': actor_rating,
        'top_genre': get_top_genre(id, connection)
    }
    return actor


def get_award_info_of_user(id, connection):
    awards = db_helper.execute_read_query(connection, get_amount_of_awards_query(id))[0][0]
    wins = db_helper.execute_read_query(connection, get_amount_of_wins_query(id))[0][0]
    last_award = db_helper.execute_read_query(connection, get_last_award_query(id))[0][0]
    return {
        'amount_awards': awards,
        'amount_wins': wins,
        'last_award': last_award
    }


def get_all_movies_of_user(id, connection):
    return


def get_movies_of(actor_id):
    connection = con.create_connection_to_scheme("localhost", "anna", "1234", "imdb")
    query = "select m.* from movies as m join actors_in_movies as am on am.movieID = m.movieID where am.actorID = '{id}' order by rating desc;".format(
        id=actor_id)
    movies_reply = db_helper.execute_read_query(connection, query)
    movies = []
    pos = 0
    for row in movies_reply:
        genres_query = "select title from genres where movieId = '{id}';".format(id=row[0])
        genres_reply = db_helper.execute_read_query(connection, genres_query)
        genre_list = [item for t in genres_reply for item in t]
        genres = ", ".join(str(genre) for genre in genre_list)
        pos = pos + 1
        movie = {
            'id': row[0],
            'pos': pos,
            'title': row[1],
            'year': row[2],
            'runtime': row[3],
            'rating': round(row[4], 2),
            'genres': genres
        }
        movies.append(movie)
    return movies





def get_awards_of(actor_id):
    connection = con.create_connection_to_scheme("localhost", "anna", "1234", "imdb")
    query = "select a.year, a.category, a.title, aha.outcome, aha.description from awards as a join actors_have_awards " \
            "as aha on aha.awardID=a.awardID where aha.actorID='{id}' order by a.year desc ;".format(id=actor_id)
    awards_reply = db_helper.execute_read_query(connection, query)
    awards = []
    for row in awards_reply:
        award = {
            'year': row[0],
            'category': row[1],
            'title': row[2],
            'outcome': row[3],
            'description': row[4],
        }
        awards.append(award)
    return awards


def get_award_wins_of(actor_id):
    connection = con.create_connection_to_scheme("localhost", "anna", "1234", "imdb")
    query = "select a.year, a.category, a.title, aha.outcome, aha.description from awards as a join actors_have_awards " \
            "as aha on aha.awardID=a.awardID where aha.actorID='{id}' and aha.outcome='winner' order by a.year desc ;".format(
        id=actor_id)
    awards_reply = db_helper.execute_read_query(connection, query)
    awards = []
    for row in awards_reply:
        award = {
            'year': row[0],
            'category': row[1],
            'title': row[2],
            'outcome': row[3],
            'description': row[4],
        }
        awards.append(award)
    return awards


def get_avg_awards():
    connection = con.create_connection_to_scheme("localhost", "anna", "1234", "imdb")
    query = "select count(*), a.year from awards as a join actors_have_awards as aha on aha.awardID=a.awardID where aha.outcome='winner' group by a.year order by a.year desc;"
    awards_reply = db_helper.execute_read_query(connection, query)
    awards_avg = {}
    for row in awards_reply:
        awards_avg.update({
            row[1]: row[0] / 50
        })
    return awards_avg


def get_avg_amounts(actor_id, amount):
    connection = con.create_connection_to_scheme("localhost", "anna", "1234", "imdb")
    reply = db_helper.execute_read_query(connection, "select count(*) from actors_have_awards where outcome='Nominee' "
                                                     "and actorID={id};".format(id=actor_id))
    nominee = reply[0][0] / amount
    reply = db_helper.execute_read_query(connection,
                                         "select count(*) from actors_have_awards where outcome='Winner' and actorID={id};".format(
                                             id=actor_id))
    winners = reply[0][0] / amount
    reply = db_helper.execute_read_query(connection,
                                         "select count(*) from actors_in_movies where actorID={id};".format(
                                             id=actor_id))
    movies = reply[0][0] / amount
    return [nominee, winners, movies]


def get_avg_movie_rating_per_year(actor_id):
    connection = con.create_connection_to_scheme("localhost", "anna", "1234", "imdb")
    reply = db_helper.execute_read_query(connection,
                                         "SELECT year, avg(nullif(m.rating,0.00)) as avg_rating, count(*) FROM movies m join actors_in_movies aim on m.movieID = aim.movieID where actorID = '{id}' and m.year!=0 group by year order by year;".format(
                                             id=actor_id))
    avg_rating_dict = {}
    for row in reply:
        if row[1] is None:
            continue

        avg_rating_dict.update(
            {row[0]: {'rating': round(row[1], 2),
                      'amount': row[2]
                      }}
        )

    #...
    query = "SELECT year, title, rating FROM movies m join actors_in_movies aim on m.movieID = aim.movieID where actorID = '{id}' and year!=0 order by year;" \
        .format(id=actor_id)
    movies_reply = db_helper.execute_read_query_dict(connection, query)
    for row in movies_reply:
        year = row['year']
        if year not in avg_rating_dict:
            continue

        entry = avg_rating_dict[year]
        if 'movies' not in entry:
            entry.update({
                'movies': list()
            })
        entry['movies'].append(row['title'] + "(" + str(row['rating']))
        #...
    return avg_rating_dict

def get_movies_for_year(actor_id):
    connection = con.create_connection_to_scheme("localhost", "anna", "1234", "imdb")
    query = "SELECT year, title, rating FROM movies m join actors_in_movies aim on m.movieID = aim.movieID where actorID = '{id}' order by year;" \
        .format(id=actor_id)
    movies_reply = db_helper.execute_read_query_dict(connection, query)
    movies = {}
    for row in movies_reply:
        year = row['year']
        if year not in movies:
            movies[year] = list()
        movies[year].append(row['title'] + " (" + str(row['rating']))
    return movies

def get_general_rating_dict():
    connection = con.create_connection_to_scheme("localhost", "anna", "1234", "imdb")
    query = "select year, avg(nullif(rating, 0)) as avg_rating from movies where year !=0 group by year order by year;"
    movies_reply = db_helper.execute_read_query_dict(connection, query)
    return movies_reply

def get_actor_name(actor_id):
    connection = con.create_connection_to_scheme("localhost", "anna", "1234", "imdb")
    query = "SELECT name from actors where actorID = '{id}';".format(id=actor_id)
    movies_reply = db_helper.execute_read_query_dict(connection, query)
    return movies_reply[0]['name']

def get_genres_of_actor(actor_id):
    connection = con.create_connection_to_scheme("localhost", "anna", "1234", "imdb")
    query = "SELECT g.title as genre, count(*) as amount FROM movies m join actors_in_movies aim on m.movieID = aim.movieID join genres g on aim.movieID = g.movieId where actorID = '{id}' group by g.title order by count(*) desc;".format(id=actor_id)
    reply = db_helper.execute_read_query_dict(connection, query)
    return reply

def get_genres_of_top_movies(actor_id):
    connection = con.create_connection_to_scheme("localhost", "anna", "1234", "imdb")
    query = "SELECT g.title as genre, count(*) as amount from (SELECT m.movieID FROM movies m join actors_in_movies aim on m.movieID = aim.movieID where actorID = '{id}' order by  m.rating desc LIMIT 5) as x join genres as g on g.movieId = x.movieID group by g.title order by count(*) desc;".format(id=actor_id)
    reply = db_helper.execute_read_query_dict(connection, query)
    return reply


get_genres_of_actor('nm0000199')

