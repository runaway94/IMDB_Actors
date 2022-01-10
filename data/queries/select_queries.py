"""select_queries.py
--------
stores all select queries

"""

get_actors_query = """
    select act.actorID, act.name, act.birthdate, AVG(rating) as rating_avg, COUNT(mov.movieID) as amount_movies, act.pos
        from actors_in_movies
        join movies as mov on actors_in_movies.movieID = mov.movieID
        join actors as act on act.actorID = actors_in_movies.actorID
        group by actors_in_movies.actorID
        order by act.pos ;
    """

best_rated_movie_query = "select title, rating from actors_in_movies " \
                         "join movies on actors_in_movies.movieID = movies.movieID " \
                         "where actors_in_movies.actorID = '{id}' " \
                         "order by rating desc limit 1;" \


newest_movie_query = "select title, year from actors_in_movies " \
                     "join movies on actors_in_movies.movieID = movies.movieID " \
                     "where actors_in_movies.actorID = '{id}' " \
                     "order by movies.year desc limit 1;"


get_actor_information_query = "select * from actors where actorID='{id}';"


select_database_query = "SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA WHERE SCHEMA_NAME = '{db_name}';"

primary_key_query = """
            SELECT k.column_name
            FROM information_schema.table_constraints t
            JOIN information_schema.key_column_usage k
            USING(constraint_name,table_schema,table_name)
            WHERE t.constraint_type='PRIMARY KEY'
            AND t.table_name='{table_name}';
        """

all_awards_of_query = """select * from awards 
                        join actors_have_awards aha 
                        on awards.awardID = aha.awardID 
                        where aha.actorID = '{actor_id}' 
                        order by year desc;"""

all_movies_of_query = """select * from movies 
                        join actors_in_movies aim 
                        on movies.movieID = aim.movieID 
                        where actorID='{actor_id}' 
                        order by rating desc;"""

genres_of_query = """select * from genres where movieId = '{movie_id}'"""

avg_awards_query = """select count(*), a.year from awards as a 
                    join actors_have_awards as aha on aha.awardID=a.awardID 
                    where aha.outcome='winner' group by a.year order by a.year desc; """

actor_name_query = "SELECT name from actors where actorID = '{actor_id}';"

all_genres_query = """SELECT g.title as genre, count(*) as amount FROM movies m 
                    join actors_in_movies aim on m.movieID = aim.movieID 
                    join genres g on aim.movieID = g.movieId 
                    where actorID = '{actor_id}' 
                    group by g.title order by count(*) desc;"""

genres_top_movies_query = """SELECT g.title as genre, count(*) as amount from (
                                SELECT m.movieID FROM movies m 
                                join actors_in_movies aim on m.movieID = aim.movieID 
                                where actorID = '{actor_id}' 
                                order by  m.rating desc LIMIT 5) as x 
                            join genres as g on g.movieId = x.movieID 
                            group by g.title order by count(*) desc;"""

avg_rating_year_query = """SELECT year, avg(nullif(m.rating,0.00)) as avg_rating, count(*) as movie_amount 
                            FROM movies m join actors_in_movies aim on m.movieID = aim.movieID 
                            where actorID ='{actor_id}' 
                            and m.year!=0 
                            group by year order by year;"""

movies_by_year_query = """SELECT year, title, rating FROM movies m 
                            join actors_in_movies aim on m.movieID = aim.movieID 
                            where actorID = '{actor_id}' 
                            and year!=0 
                            order by year;"""

general_rating_query ="""select year, avg(nullif(rating, 0)) as avg_rating 
                        from movies where year !=0 
                        group by year order by year;"""