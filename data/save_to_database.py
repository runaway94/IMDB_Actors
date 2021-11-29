from IMDB_Actors.data import db_helper as con, db_helper
from IMDB_Actors.data import queries


def save_actor(actor):
    connection = con.create_connection_to_scheme("localhost", "anna", "1234", "imdb")
    query = queries.insert_into_query("actors", actor)
    db_helper.execute_query(connection, query)


def save_awards(award):
    connection = con.create_connection_to_scheme("localhost", "anna", "1234", "imdb")

    get_award_query = queries.get_id_from_award(award["category"], award["year"], award["title"])
    award_reply = db_helper.execute_read_query(connection, get_award_query)

    if len(award_reply) == 0:
        save_obj = {
            "title": award["title"],
            "year": award["year"],
            "category": award["category"]
        }
        save_award_query = queries.insert_into_query("awards", save_obj)
        db_helper.execute_query(connection, save_award_query)
        award_reply = db_helper.execute_read_query(connection, get_award_query)

    id = award_reply[0][0]


    save_link_obj = {
        "actorID": award["actor"],
        "outcome": award["outcome"],
        "awardID": id,
        "description": award["description"]
    }
    save_con_qu = queries.insert_into_query("actors_have_awards", save_link_obj)
    db_helper.execute_query(connection, save_con_qu)


def save_movie(movie):
    connection = con.create_connection_to_scheme("localhost", "anna", "1234", "imdb")

    is_already_saved_query = queries.is_movie_in_database(movie["movieID"])
    amount = db_helper.execute_read_query(connection, is_already_saved_query)
    actor = movie["actor"]
    del movie["actor"]
    genres = []
    if "genres" in movie.keys():
        genres = movie["genres"]
        del movie["genres"]

    if amount[0][0] == 0:
        save_award_query = queries.insert_into_query("movies", movie)
        db_helper.execute_query(connection, save_award_query)

    # save genre
    for genre in genres:
        save_genre_obj = {
            "title": "\'" + genre + "\'",
            "movieID": movie["movieID"]
        }
        query = queries.insert_into_query("genres", save_genre_obj)
        db_helper.execute_query(connection, query)

    # link movie to actor
    act_obj = {
        "actorID": actor,
        "movieID": movie["movieID"]
    }

    query = queries.insert_into_query("actors_in_movies", act_obj)
    db_helper.execute_query(connection, query)
