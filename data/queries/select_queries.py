def get_all(database):
    query = "SELECT * FROM imdb.awards {database};".format(
        database=database)
    return query



get_auctors_query = """
    select act.actorID, act.name, act.birthdate, AVG(rating) as avg, COUNT(mov.movieID), act.pos
        from actors_in_movies 
        join movies as mov on actors_in_movies.movieID = mov.movieID 
        join actors as act on act.actorID = actors_in_movies.actorID 
        group by actors_in_movies.actorID 
        order by act.pos ;
    """


def get_best_rated_movie(actorID):
    query = "select title, rating from actors_in_movies " \
            "join movies on actors_in_movies.movieID = movies.movieID " \
            "where actors_in_movies.actorID = '{id}' " \
            "order by rating desc limit 1;"\
        .format(id=actorID)
    return query

def get_newest_movie_query(actorID):
    query = "select title, year from actors_in_movies " \
            "join movies on actors_in_movies.movieID = movies.movieID " \
            "where actors_in_movies.actorID = '{id}' " \
            "order by movies.year desc limit 1;"\
        .format(id=actorID)
    return query


def get_actor_information_query(actorID):
    query = "select * from actors where actorID='{id}';".format(id=actorID)
    return query

def get_all_movies_of_actor_query(actorID):
    query = "select movies.* from actors_in_movies " \
            "left join movies on actors_in_movies.movieID = movies.movieIDgenresgenresgenres " \
            "where actors_in_movies.actorID = '{id}'" \
            "order by rating desc;".format(id=actorID)
    return query

def get_amount_of_wins_query(actorID):
    query = "select count(*) from actors_have_awards " \
             "left join awards on actors_have_awards.awardID = awards.awardID " \
             "where actors_have_awards.actorID = '{id}' " \
             "AND outcome = 'winner';".format(id=actorID)
    return query

def get_amount_of_awards_query(actorID):
    query = "select count(*) from actors_have_awards " \
            "left join awards on actors_have_awards.awardID = awards.awardID " \
            "where actors_have_awards.actorID = '{id}';".format(id=actorID)
    return query

def get_last_award_query(actorID):
    query = "select awards.category from actors_have_awards " \
            "left join awards on actors_have_awards.awardID = awards.awardID " \
            "where actors_have_awards.actorID = '{id}' AND outcome = 'winner' " \
            "order by year desc limit 1;".format(id=actorID)
    return query