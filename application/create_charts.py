import collections
from collections import Counter

import pandas as pd
import pylab
from matplotlib import pyplot as plt
from wordcloud import WordCloud

from IMDB_Actors.data.get_from_database import get_awards_of, get_avg_awards, \
    get_avg_amounts, get_avg_movie_rating_per_year, get_general_rating_dict, get_actor_name, get_genres_of_actor, \
    get_genres_of_top_movies, get_movies_of

pie_chart_path = "../presentation/static/images/movie_charts/movies_piechart_{id}.png"
wordcloud_path = "../presentation/static/images/movie_charts/movies_wordcloud_{id}.png"
movie_rating_path = "../presentation/static/images/movie_charts/movies_rating_per_year_{id}.png"
movie_rating_comp_path = "../presentation/static/images/movie_charts/ratings_compared_{id}.png"
award_path = "../presentation/static/images/award_charts/award_charts_{id}.png"
award_compare_path = "../presentation/static/images/award_charts/award_compare_charts_{id}.png"
general_chart_path = "../presentation/static/images/charts/charts_{id}.png"


def genres_pie_chart(actor_id):
    genres = get_genres_of_top_movies(actor_id)
    df = pd.DataFrame(genres)
    df = df.set_index('genre')
    df.plot.pie(y='amount', autopct='%1.1f%%', legend=None)
    pylab.ylabel('')
    pie_path = pie_chart_path.format(id=actor_id)
    plt.savefig(pie_path)
    plt.close()
    return df.to_dict()['amount']


def genres_wordcloud_chart(actor_id):
    genres = get_genres_of_actor(actor_id)
    df = pd.DataFrame(genres)
    df = df.set_index('genre')
    wordcloud = WordCloud(background_color="white")
    dic = df.to_dict()['amount']
    wordcloud.generate_from_frequencies(frequencies=dic)
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    path = wordcloud_path.format(id=actor_id)
    plt.savefig(path)
    plt.close()
    return dic


def awards_plot(actor_id):
    awards = get_awards_of(actor_id)
    award_wins = [award for award in awards if award['outcome'] == 'Winner']
    movies = get_movies_of(actor_id)
    ax = plt.subplot()

    awards_per_year = Counter(award['year'] for award in awards)
    df_awards = pd.DataFrame.from_dict(awards_per_year, orient='index').reindex(range(1964, 2022)).fillna(0)
    ax.plot(df_awards, label='awards per year')

    award_wins_per_year = Counter(award['year'] for award in award_wins)
    df_wins = pd.DataFrame.from_dict(award_wins_per_year, orient='index').reindex(range(1964, 2022)).fillna(0)
    ax.plot(df_wins, label='wins per year')

    movies_per_year = Counter(movie['year'] for movie in movies)
    movies_per_year = collections.OrderedDict(sorted(movies_per_year.items()))
    if 0 in movies_per_year:
        movies_per_year.pop(0)
    df_movies = pd.DataFrame.from_dict(movies_per_year, orient='index').reindex(range(1964, 2022)).fillna(0)
    ax.plot(df_movies, label='movies per year')

    ax.set_xlabel("year")
    ax.set_ylabel("amount")
    ax.legend(loc='best')

    path = award_path.format(id=actor_id)
    plt.savefig(path)
    plt.close()


def avg_awards_plot(actor_id):
    awards = get_awards_of(actor_id)
    actor_wins = [award for award in awards if award['outcome'] == 'Winner']
    avg_wins = get_avg_awards()
    print(avg_wins)
    ax = plt.subplot()
    ax.plot(*zip(*sorted(avg_wins.items())), label='average awards per year', color='#343A40')

    award_wins_per_year = Counter(award['year'] for award in actor_wins)
    df_wins = pd.DataFrame.from_dict(award_wins_per_year, orient='index').reindex(range(1964, 2022)).fillna(0)
    print(df_wins)
    ax.plot(df_wins, label='wins of actor', color="#f6c800")

    ax.set_xlabel("year")
    ax.set_ylabel("amount")
    ax.legend(loc='best')
    path = award_compare_path.format(id=actor_id)

    plt.savefig(path)

    plt.close()


def avg_awards_movies_bar(actor_id):
    index = ["nominations", "wins", "movies"]
    avg_awards_amount = get_avg_amounts("actorID", 50)
    actor_awards_amount = get_avg_amounts("\'" + actor_id + "\'", 1)
    print(avg_awards_amount)
    print(actor_awards_amount)

    plotdata = pd.DataFrame({
        "average": avg_awards_amount,
        "actor": actor_awards_amount,
    },
        index=index
    )
    plotdata.plot(kind="bar", rot=0, color={'average': '#343A40', 'actor': '#f6c800'})
    plt.title("movies and awards in comparison to average")
    plt.ylabel("Amount")
    path = general_chart_path.format(id=actor_id)
    plt.savefig(path)
    print(plotdata.to_dict())
    plt.close()
    return plotdata.to_dict()


def movie_rating_per_year(actor_id):
    ax = plt.gca()
    dic = get_general_rating_dict()
    df = pd.DataFrame(dic)
    df = df.set_index('year')
    avg_rating_dict = get_avg_movie_rating_per_year(actor_id)
    df_movie_ratings = pd.DataFrame.from_dict(avg_rating_dict, orient='index')
    df = df.join(df_movie_ratings['rating'])
    df = df[df.avg_rating.notnull()]
    df = df[df.rating.notnull()]
    df = df.astype(float)
    plt.ylabel("rating")
    actor = get_actor_name(actor_id)
    df.plot(kind='line', ax=ax, y='rating', label=actor, color='#f6c800')
    plt.title("Average movie rating per year")
    path = movie_rating_path.format(id=actor_id)
    plt.savefig(path)
    plt.title("Average rating compared to other actors")
    df.plot(kind='line', ax=ax, y='avg_rating', label="all actors", color='#343A40')
    path = movie_rating_comp_path.format(id=actor_id)
    plt.savefig(path)
    plt.close()

    return avg_rating_dict
