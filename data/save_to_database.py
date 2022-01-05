from IMDB_Actors.data.db_connection import Connection


def persist_information(actor):
    con = Connection()

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

    print(f"{actor.name} saved")
