"""get_from_database.py
--------
"""
from IMDB_Actors.data.db_connection import Connection
from IMDB_Actors.data.queries.select_queries import *


def get_all_actors():
    """Returns List of all actors

    :returns list of all actors
    :rtype: list(dict)
    """
    con = Connection()
    reply = con.execute_read_query(get_actors_query)
    for actor in reply:
        actor["rating_avg"] = str(round(actor["rating_avg"], 2))
        actor["pop_movie"] = get_pop_movie(actor["actorID"], con)
        actor["new_movie"] = get_new_movie(actor["actorID"], con)
    return reply


def get_pop_movie(actor_id, con):
    """extracts most popular movie of a specific actor

    :param con: Database Connection
    :type con: Connection
    :param actor_id: actorID of actor
    :type actor_id: str
    :returns: most popular movie of specific actor as dict
    :rtype: dict
    """
    query = best_rated_movie_query.format(id=actor_id)
    best_rated_mov_repl = con.execute_read_query(query)
    title = best_rated_mov_repl[0]['title']
    rating = best_rated_mov_repl[0]['rating']
    return title + " (" + str(rating)[:3] + ")"


def get_new_movie(actor_id, con):
    """extracts newest movie of a specific actor

    :param con: Database Connection
    :type con: Connection
    :param actor_id: actorID of actor
    :type actor_id: str
    :returns: newest movie of specific actor as dict
    :rtype: dict
    """
    new_mov_repl = con.execute_read_query(newest_movie_query.format(id=actor_id))
    title = new_mov_repl[0]['title']
    year = new_mov_repl[0]['year']
    return title + " (" + str(year) + ")"


def get_single_actor(actor_id):
    """extracts information of a specific actor

    :param actor_id: actorID of actor
    :type actor_id: str
    :returns: all information of one specific actor needed for the 'about' page
    :rtype: dict
    """
    con = Connection()
    actor = con.execute_read_query(get_actor_information_query.format(id=actor_id))[0]

    # awards
    award_info = get_awards_of(actor_id, con)
    wins = len([award for award in award_info if award['outcome'] == 'Winner'])
    last_award = f"{award_info[0]['title']} ({award_info[0]['year']})"
    actor.update({
        'amount_awards': len(award_info),
        'amount_wins': wins,
        'last_award': last_award
    })

    # movies
    movie_info = get_movies_of(actor_id, con)
    top_movie = f"{movie_info[0]['title']} ({movie_info[0]['rating']})"
    movies_sorted_by_year = sorted(movie_info, key=lambda i: i['year'])
    newest_movie = f"{movies_sorted_by_year[-1]['title']} ({movies_sorted_by_year[-1]['year']})"

    genres_list = [d['genres'] for d in movie_info]
    genres = [item for sublist in genres_list for item in sublist]
    top_genre_title = max(set(genres), key=genres.count)
    top_genre = f"{top_genre_title} ({genres.count(top_genre_title)})"
    rating = round(sum(d['rating'] for d in movie_info) / len(movie_info), 2)
    actor.update({
        'amount_movies': len(movie_info),
        'new_movie': newest_movie,
        'top_movie': top_movie,
        'top_rating': movie_info[0]['rating'],
        'rating': rating,
        'top_genre': top_genre
    })
    return actor


def get_awards_of(actor_id, con=None):
    """extracts awards of a specific actor

    :param con: Database Connection
    :type con: Connection
    :param actor_id: actorID of actor
    :type actor_id: str
    :returns: all awards of specific actor
    :rtype: list(dict)
    """
    if con is None:
        con = Connection()
    awards = con.execute_read_query(all_awards_of_query.format(actor_id=actor_id))
    return awards


def get_movies_of(actor_id, con=None):
    """extracts all movies of a specific actor

    :param con: Database Connection
    :type con: Connection
    :param actor_id: actorID of actor
    :type actor_id: str
    :returns: all movies of specific actor
    :rtype: list(dict)
    """
    if con is None:
        con = Connection()
    movies = con.execute_read_query(all_movies_of_query.format(actor_id=actor_id))
    for movie in movies:
        genres_reply = con.execute_read_query(genres_of_query.format(movie_id=movie['movieID']))
        genres = [d['title'] for d in genres_reply]
        movie.update({
            'genres': genres,
            'genres_readable': ', '.join(genres)
        })

    return movies


def get_avg_awards():
    """extracts average awards of all actors

    :returns: average awards of all actors
    :rtype: dict
    """
    con = Connection()
    awards_reply = con.execute_read_query(avg_awards_query, False)
    awards_avg = {}
    for row in awards_reply:
        awards_avg.update({
            row[1]: row[0] / 50
        })
    return awards_avg


def get_avg_amounts(actor_id, amount=None):
    """extracts average nominations, movies and wins of one or all actors

    :param amount: amount of all actors (default is None)
    :type amount: int
    :param actor_id: actorID of actor
    :type actor_id: str
    :returns: list of results
    :rtype: list
    """
    con = Connection()
    awards = con.execute_read_query(f"select * from actors_have_awards where actorID={actor_id};")
    winners = len([award for award in awards if award['outcome'] == 'Winner'])
    nominee = (len(awards) - winners)
    winners = winners

    reply = con.execute_read_query(f"select count(*) as count from actors_in_movies where actorID={actor_id};")
    movies = reply[0]['count']
    if amount is not None:
        nominee = nominee / amount
        winners = winners / amount
        movies = movies / amount
    return [nominee, winners, movies]


def get_avg_movie_rating_per_year(actor_id):
    """extracts average movie rating of of specific actor per year

    :param actor_id: actorID of actor
    :type actor_id: str
    :returns: average movie rating of of specific actor per year
    :rtype: dict
    """
    con = Connection()
    reply = con.execute_read_query(avg_rating_year_query.format(actor_id=actor_id))
    avg_rating_dict = {}
    for row in reply:
        if row['year'] is None or row['avg_rating'] is None:
            continue

        avg_rating_dict.update(
            {row['year']: {'rating': round(row['avg_rating'], 2),
                           'amount': row['movie_amount']
                           }}
        )
    movies_reply = con.execute_read_query(movies_by_year_query.format(actor_id=actor_id))
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
    return avg_rating_dict


def get_general_rating_dict():
    """extracts average movie rating of all actors per year

    :returns: average movie rating of of all actors per year
    :rtype: dict
    """
    con = Connection()
    movies_reply = con.execute_read_query(general_rating_query)
    return movies_reply


def get_actor_name(actor_id):
    """
    :param actor_id: actorID of actor
    :type actor_id: str
    :returns: name of actor
    :rtype: str
    """
    con = Connection()
    movies_reply = con.execute_read_query(actor_name_query.format(actor_id=actor_id))
    return movies_reply[0]['name']


def get_genres_of_actor(actor_id):
    """
    :param actor_id: actorID of actor
    :type actor_id: str
    :returns: all genres of one actor
    :rtype: list
    """
    con = Connection()
    reply = con.execute_read_query(all_genres_query.format(actor_id=actor_id))
    return reply


def get_genres_of_top_movies(actor_id):
    """
    :param actor_id: actorID of actor
    :type actor_id: str
    :returns: genres of top movies of one actor
    :rtype: list
    """
    con = Connection()
    reply = con.execute_read_query(genres_top_movies_query.format(actor_id=actor_id))
    return reply

