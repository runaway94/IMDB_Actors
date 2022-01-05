from IMDB_Actors.data.db_connection import Connection
from IMDB_Actors.data.queries.select_queries import *


def get_all_actors():
    con = Connection()
    reply = con.execute_read_query(get_auctors_query)
    for actor in reply:
        actor["rating_avg"] = str(round(actor["rating_avg"], 2))
        actor["pop_movie"] = get_pop_movie(actor["actorID"], con)
        actor["new_movie"] = get_new_movie(actor["actorID"], con)
    return reply


def get_pop_movie(actor_id, con):
    best_mov_qu = get_best_rated_movie(actor_id)
    best_rated_mov_repl = con.execute_read_query(best_mov_qu)
    title = best_rated_mov_repl[0]['title']
    rating = best_rated_mov_repl[0]['rating']
    return title + " (" + str(rating)[:3] + ")"


def get_new_movie(actor_id, con):
    new_mov_qu = get_newest_movie_query(actor_id)
    new_mov_repl = con.execute_read_query(new_mov_qu)
    title = new_mov_repl[0]['title']
    year = new_mov_repl[0]['year']
    return title + " (" + str(year) + ")"


def get_single_actor(actor_id):
    query = get_actor_information_query(actor_id)
    con = Connection()
    actor = con.execute_read_query(query)[0]

    # awards
    award_info = get_awards_of(actor_id, con)
    wins = len([award for award in award_info if award['outcome'] == 'Winner'])
    last_award = f"{award_info[0]['title']} ({award_info[0]['year']})"
    actor.update({
        'amount_awards': wins,
        'amount_wins': len(award_info) - wins,
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
    print(actor)
    return actor


def get_awards_of(actor_id, con=None):
    if con is None:
        con = Connection()
    query = f"select * from awards join actors_have_awards aha on awards.awardID = aha.awardID where aha.actorID = '{actor_id}' order by year desc "
    awards = con.execute_read_query(query)
    return awards


def get_movies_of(actor_id, con=None):
    if con is None:
        con = Connection()
    query = f"select * from movies join actors_in_movies aim on movies.movieID = aim.movieID where actorID='{actor_id}' order by rating desc;"
    movies = con.execute_read_query(query)
    for movie in movies:
        query = f"select * from genres where movieId = '{movie['movieID']}'"
        genres_reply = con.execute_read_query(query)
        genres = [d['title'] for d in genres_reply]
        movie.update({
            'genres': genres,
            'genres_readable': ', '.join(genres)
        })

    return movies


def get_avg_awards():
    con = Connection()
    query = "select count(*), a.year from awards as a join actors_have_awards as aha on aha.awardID=a.awardID where " \
            "aha.outcome='winner' group by a.year order by a.year desc; "
    awards_reply = con.execute_read_query(query, False)
    awards_avg = {}
    for row in awards_reply:
        awards_avg.update({
            row[1]: row[0] / 50
        })
    return awards_avg


def get_avg_amounts(actor_id, amount):
    con = Connection()
    awards = con.execute_read_query(f"select * from actors_have_awards where actorID={actor_id};")
    winners = len([award for award in awards if award['outcome'] == 'Winner'])
    nominee = (len(awards) - winners) / amount
    winners = winners / 50
    reply = con.execute_read_query(f"select count(*) as count from actors_in_movies where actorID={actor_id};")
    movies = reply[0]['count'] / amount
    return [nominee, winners, movies]


def get_avg_movie_rating_per_year(actor_id):
    con = Connection()
    rating_query = f"SELECT year, avg(nullif(m.rating,0.00)) as avg_rating, count(*) as movie_amount FROM movies m join actors_in_movies aim on m.movieID = aim.movieID where actorID ='{actor_id}' and m.year!=0 group by year order by year;";
    reply = con.execute_read_query(rating_query)
    avg_rating_dict = {}
    for row in reply:
        if row['year'] is None or row['avg_rating'] is None:
            continue

        avg_rating_dict.update(
            {row['year']: {'rating': round(row['avg_rating'], 2),
                           'amount': row['movie_amount']
                           }}
        )
    movie_query = f"SELECT year, title, rating FROM movies m join actors_in_movies aim on m.movieID = aim.movieID where actorID = '{actor_id}' and year!=0 order by year;"
    movies_reply = con.execute_read_query(movie_query)
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
    con = Connection()
    query = "select year, avg(nullif(rating, 0)) as avg_rating from movies where year !=0 group by year order by year;"
    movies_reply = con.execute_read_query(query)
    return movies_reply


def get_actor_name(actor_id):
    con = Connection()
    query = f"SELECT name from actors where actorID = '{actor_id}';"
    movies_reply = con.execute_read_query(query)
    return movies_reply[0]['name']


def get_genres_of_actor(actor_id):
    con = Connection()
    query = f"SELECT g.title as genre, count(*) as amount FROM movies m join actors_in_movies aim on m.movieID = aim.movieID join genres g on aim.movieID = g.movieId where actorID = '{actor_id}' group by g.title order by count(*) desc;"
    reply = con.execute_read_query(query)
    return reply


def get_genres_of_top_movies(actor_id):
    con = Connection()
    query = f"SELECT g.title as genre, count(*) as amount from (SELECT m.movieID FROM movies m join actors_in_movies aim on m.movieID = aim.movieID where actorID = '{actor_id}' order by  m.rating desc LIMIT 5) as x join genres as g on g.movieId = x.movieID group by g.title order by count(*) desc;";
    reply = con.execute_read_query(query)
    return reply

