"""save_to_database.py
--------
"""
from IMDB_Actors.data.db_connection import Connection


def persist_information(actor):
    """saves actor in database, as well as his awards and the movies he played in

    :param actor: actor to save in db
    :type actor: Actor
    """
    try:
        con = Connection()
    except (FileNotFoundError, ConnectionError):
        print("Connection to database failed. Please check your configurations.")
        print(f"Failed to save {actor.name}")
        return

    # save actor
    actor_info = actor.get_actor_information()
    con.save_value(actor_info, 'actors')

    # save awards
    for award in actor.awards:
        award_info = award.get_award_info()
        con.save_value(award_info, 'awards', award.awardID)

        award_actor_link = award.get_linking_information()
        award_actor_link["actorID"] = actor_info["actorID"]
        con.save_value(award_actor_link, 'actors_have_awards')

    # save movies
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

