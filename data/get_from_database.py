from IMDB_Actors.data import db_helper as con, db_helper
from IMDB_Actors.data.queries.select_queries import *


def get_actor_for_table():
    connection = con.create_connection_to_scheme("localhost", "anna", "1234", "imdb")
    actor_reply = db_helper.execute_read_query(connection, get_auctors_query)
    actors = []
    for row in actor_reply:
        id = row[0]
        best_movie = get_most_popular_movie(id, connection)
        new_movie = get_newest_movie(id, connection)
        actor = {
            'id': row[0],
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
    print(best_rated_mov_repl)
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
    query = "select avg(rating) from actors_in_movies join movies on actors_in_movies.movieID = movies.movieID where actors_in_movies.actorID = '{id}';".format(id=id)
    repl = db_helper.execute_read_query(connection, query)
    return repl[0][0]

def get_top_genre(id, connection):
    query = "select count(*) as amount, title from actors_in_movies join genres on genres.movieId = actors_in_movies.movieID where actors_in_movies.actorID = '{id}' group by title order by amount desc limit 1;".format(id=id)
    repl = db_helper.execute_read_query(connection, query)
    genre = str(repl[0][1]) + " (" + str(repl[0][0]) + ")"
    return genre

def get_single_actor(id):
    query = get_actor_information_query(id)
    connection = con.create_connection_to_scheme("localhost", "anna", "1234", "imdb")
    actor_reply = db_helper.execute_read_query(connection, query)
    #print(actor_reply)
    row = actor_reply[0]
    award_info = get_award_info_of_user(id, connection)
    #print(award_info)
    gender = ""
    if row[5] == 0:
        gender = "male"
    else:
        gender = "female"
    new_movie = get_newest_movie(id, connection)
    top_movie = get_most_popular_movie(id, connection)
    s = top_movie.index('(') + 1
    top_rating = top_movie[s:-1]
    movies = get_movie_amount(id, connection)
    actor_rating = get_actor_rating(id, connection)
    actor_rating = round(actor_rating, 2)

    # add movies

    # add awards

    actor = {
        'id': row[0],
        'name': row[1],
        'birth': row[2],
        'image': row[3],
        'bio': row[4],
        'gender': gender,
        'pos': row[6],
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



