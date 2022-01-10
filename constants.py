"""constants.py
--------
contains string constant"""

# Path to database configuration
db_config = "data/db_config.json"

# Paths to charts
movie_pie_chart = "presentation/static/images/movie_charts/movies_piechart_{id}.png"
genre_wordcloud = "presentation/static/images/movie_charts/movies_wordcloud_{id}.png"
movie_rating_per_year_path = "presentation/static/images/movie_charts/movies_rating_per_year_{id}.png"
movie_rating_compared = "presentation/static/images/movie_charts/ratings_compared_{id}.png"
award_chart = "presentation/static/images/award_charts/award_charts_{id}.png"
award_compared = "presentation/static/images/award_charts/award_compare_charts_{id}.png"
general_chart = "presentation/static/images/charts/charts_{id}.png"

# IMDb links
imbd_list_top_actors = "https://www.imdb.com/list/ls053501318/"
actor_detail_url = "https://www.imdb.com/name/{actorID}"
actor_bio_url = "https://www.imdb.com/name/{actorID}/bio"
actress_movies_url = "https://www.imdb.com/filmosearch/?role={actorID}&sort=moviemeter," \
                     "asc&job_type=actress&title_type=movie&title_type=short&title_type=musicVideo&title_type=" \
                     "video&title_type=tvMovie "
actor_movie_url = "https://www.imdb.com/filmosearch/?role={actorID}&sort=moviemeter," \
                  "asc&job_type=actor&title_type=movie&title_type=short&title_type=musicVideo&title_type=video" \
                  "&title_type=tvMovie "
award_URL = "https://www.imdb.com/name/{actorID}/awards?ref_=nm_ql_2"



