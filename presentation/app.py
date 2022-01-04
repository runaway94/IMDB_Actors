from flask import Flask, render_template, request

from IMDB_Actors.application.create_charts import create_charts, create_awards_per_year, create_awards_avg, \
    general_avg_chart, movie_rating_per_year, temp2, temp
from IMDB_Actors.data.get_from_database import get_actor_for_table, get_single_actor, get_movies_of, get_awards_of

app = Flask(__name__)


@app.route('/')
def actors():  # put application's code here
    actors = get_actor_for_table();
    print(actors)
    return render_template('actors.html', actorTableEntrys=actors)


@app.route('/actor')
def actor():
    actor_id = request.args.get('id', default=1, type=str)
    actor = get_single_actor(actor_id)
    chart_info = general_avg_chart(actor_id)
    return render_template('actor_detail.html', actor=actor, chart_info=chart_info)


@app.route('/movies')
def movies():
    actor_id = request.args.get('id', default=1, type=str)
    movies = get_movies_of(actor_id)
    actor = get_single_actor(actor_id)
    #create_charts(movies, actor_id)
    top_genres = temp(actor_id)
    all_genres = temp2(actor_id)

    avg_rating_per_year = movie_rating_per_year(actor_id)
    return render_template('actor_movies.html', actor=actor, movies=movies, len=len(movies),
                           rating_per_year=avg_rating_per_year, top_genres=top_genres, all_genres=all_genres)


@app.route('/awards')
def awards():
    actor_id = request.args.get('id', default=1, type=str)
    awards = get_awards_of(actor_id)
    actor = get_single_actor(actor_id)
    create_awards_per_year(actor_id)
    create_awards_avg(actor_id)
    return render_template('actor_awards.html', actor=actor, awards=awards, len=len(awards))


if __name__ == '__main__':
    app.run()
