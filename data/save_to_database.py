from IMDB_Actors.data import db_helper as con, db_helper
from IMDB_Actors.data.db_connection import Connection
from IMDB_Actors.data.queries import insert_queries


# def save_actor(actor):
#     connection = con.create_connection_to_scheme("localhost", "anna", "1234", "imdb")
#     query = insert_queries.insert_into_query("actors", actor)
#     db_helper.execute_query(connection, query)

def save_actor(con, actor):
    query = insert_queries.insert_into_query("actors", actor)
    con.execute_query(query)

def save_award(con, award):
    pass



def save_award_link(award_actor_link):
    pass


def persist_information(actor):
    con = Connection()
    actor_info = actor.get_actor_information()
    con.save_value(actor_info, 'actors')

    for award in actor.awards:
        award_info = award.get_award_info()
        con.save_value(award_info, 'awards', award.awardID)

        award_actor_link = award.get_linking_information()
        award_actor_link["actorID"] = actor_info["actorID"]
        con.save_value(award_actor_link, 'actors_have_awards')
        save_award_link(award_actor_link)

    for movie in actor.movies:
        movie_info = movie.get_movie_information()
        is_new_entry = con.save_value(movie_info, 'movies', movie.movieID)
        if is_new_entry:
            genres = movie.get_genres()
            for genre in genres:
                con.save_value(genre, 'genres')

        movie_actor_link = {
            "actorID": actor_info['actorID'],
            "movieID": movie_info['movieID'],
        }
        con.save_value(movie_actor_link, 'actors_in_movies')

    print(f"{actor.name} saved")


def save_awards(award):
    connection = con.create_connection_to_scheme("localhost", "anna", "1234", "imdb")

    get_award_query = insert_queries.get_id_from_award(award["category"], award["year"], award["title"])
    award_reply = db_helper.execute_read_query(connection, get_award_query)

    if len(award_reply) == 0:
        save_obj = {
            "title": award["title"],
            "year": award["year"],
            "category": award["category"]
        }
        save_award_query = insert_queries.insert_into_query("awards", save_obj)
        db_helper.execute_query(connection, save_award_query)
        award_reply = db_helper.execute_read_query(connection, get_award_query)

    id = award_reply[0][0]

    save_link_obj = {
        "actorID": award["actor"],
        "outcome": award["outcome"],
        "awardID": id,
        "description": award["description"]
    }
    save_con_qu = insert_queries.insert_into_query("actors_have_awards", save_link_obj)
    db_helper.execute_query(connection, save_con_qu)


def save_movie(movie):
    connection = con.create_connection_to_scheme("localhost", "anna", "1234", "imdb")

    is_already_saved_query = insert_queries.is_movie_in_database(movie["movieID"])
    amount = db_helper.execute_read_query(connection, is_already_saved_query)
    actor = movie["actor"]
    del movie["actor"]
    genres = []
    if "genres" in movie.keys():
        genres = movie["genres"]
        del movie["genres"]

    if amount[0][0] == 0:
        save_award_query = insert_queries.insert_into_query("movies", movie)
        db_helper.execute_query(connection, save_award_query)

        # save genre
        for genre in genres:
            genre = genre.strip()
            save_genre_obj = {
                "title": "\'" + genre + "\'",
                "movieID": movie["movieID"]
            }
            query = insert_queries.insert_into_query("genres", save_genre_obj)
            db_helper.execute_query(connection, query)

    # link movie to actor
    act_obj = {
        "actorID": actor,
        "movieID": movie["movieID"]
    }

    query = insert_queries.insert_into_query("actors_in_movies", act_obj)
    db_helper.execute_query(connection, query)

test = {
    "a" : 1,
    "b" : 2
}
h =hash(frozenset(test.items()))
# print(h)
# {'title': "'Washington DC Area Film Critics Association Awards'", 'year': '2019', 'category': "'WAFCA Award'", 'awardID': 90549437}
# {'title': "'Washington DC Area Film Critics Association Awards'", 'year': '2011', 'category': "'WAFCA Award'", 'awardID': 35831080}
# {'title': "'Western Heritage Awards'", 'year': '1995', 'category': "'Bronze Wrangler'", 'awardID': 4751708}
# {'title': "'Yoga Awards'", 'year': '2005', 'category': "'Yoga Award'", 'awardID': 89657952}
# {'title': "'Yoga Awards'", 'year': '2000', 'category': "'Yoga Award'", 'awardID': 47103644}