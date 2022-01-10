"""create_charts.py
--------
"""

import collections
import os
from collections import Counter

import pandas as pd
import pylab
from matplotlib import pyplot as plt
from wordcloud import WordCloud

from IMDB_Actors.constants import genre_wordcloud, award_chart, award_compared, general_chart, movie_rating_compared, \
    movie_pie_chart, movie_rating_per_year_path
from IMDB_Actors.data.get_from_database import get_genres_of_actor, get_genres_of_top_movies, get_awards_of, \
    get_movies_of, get_avg_awards, get_actor_name, get_avg_amounts, get_general_rating_dict, \
    get_avg_movie_rating_per_year


def genres_pie_chart(actor_id):
    """Generates a pie chart of all genres of the top 5 movies with one actor and saves the chart

    :param actor_id: id of actor
    :type actor_id: str
    :returns: dataframe of chart
    :rtype: dict
    """
    genres = get_genres_of_top_movies(actor_id)
    df = pd.DataFrame(genres)
    df = df.set_index('genre')
    pie_path = movie_pie_chart.format(id=actor_id)
    if os.path.isfile(pie_path):
        return df.to_dict()['amount']
    df.plot.pie(y='amount', autopct='%1.1f%%', legend=None)
    pylab.ylabel('')
    plt.savefig(pie_path)
    plt.close()
    return df.to_dict()['amount']


def genres_wordcloud_chart(actor_id):
    """Generates a word cloud of all genres of all 5 movies with one actor and saves the word cloud

    :param actor_id: id of actor
    :type actor_id: str
    :returns: dataframe of chart
    :rtype: dict
    """
    genres = get_genres_of_actor(actor_id)
    df = pd.DataFrame(genres)
    df = df.set_index('genre')
    dic = df.to_dict()['amount']
    path = genre_wordcloud.format(id=actor_id)
    if os.path.isfile(path):
        return dic
    wordcloud = WordCloud(background_color="white")
    wordcloud.generate_from_frequencies(frequencies=dic)
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.savefig(path)
    plt.close()
    return dic


def awards_plot(actor_id):
    """Generates a plot of all awards the actor has won and was nominated over the years as well as the movies he played

    :param actor_id: id of actor
    :type actor_id: str
    """
    path = award_chart.format(id=actor_id)
    if os.path.isfile(path):
        return
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

    plt.savefig(path)
    plt.close()


def avg_awards_plot(actor_id):
    """Generates a plot of all awards the actor has won in comparison to the other top 50 actors and saves the chart

    :param actor_id: id of actor
    :type actor_id: str
    """
    path = award_compared.format(id=actor_id)
    if os.path.isfile(path):
        return
    awards = get_awards_of(actor_id)
    actor_wins = [award for award in awards if award['outcome'] == 'Winner']
    avg_wins = get_avg_awards()
    ax = plt.subplot()
    ax.plot(*zip(*sorted(avg_wins.items())), label='average awards per year', color='#343A40')

    award_wins_per_year = Counter(award['year'] for award in actor_wins)
    df_wins = pd.DataFrame.from_dict(award_wins_per_year, orient='index').reindex(range(1964, 2022)).fillna(0)
    name = get_actor_name(actor_id)
    ax.plot(df_wins, label=f'wins of {name}', color="#f6c800")

    ax.set_xlabel("year")
    ax.set_ylabel("amount")
    ax.legend(loc='best')

    plt.savefig(path)

    plt.close()


def avg_awards_movies_bar(actor_id):
    """ Generates a bar chart of all awards the actor has won or was nominated for and the amount of movies he played in
    in comparison to the other actors and saves the chart

    :param actor_id: id of actor
    :type actor_id: str
    :returns: plot data of chart
    :rtype: dict
    """
    index = ["nominations", "wins", "movies"]
    avg_awards_amount = get_avg_amounts("actorID", 50)
    actor_awards_amount = get_avg_amounts("\'" + actor_id + "\'")
    plotdata = pd.DataFrame({
        "average": avg_awards_amount,
        "actor": actor_awards_amount,
    },
        index=index
    )
    path = general_chart.format(id=actor_id)
    if os.path.isfile(path):
        return plotdata.to_dict()
    plotdata.plot(kind="bar", rot=0, color={'average': '#343A40', 'actor': '#f6c800'})
    plt.title("movies and awards in comparison to average")
    plt.ylabel("Amount")
    plt.savefig(path)
    plt.close()
    return plotdata.to_dict()


def movie_rating_per_year(actor_id):
    """Generates a plot of the ratings of the movies the actor played in over the years (in comparison to the other actors)
    and saves the chart

    :param actor_id: id of actor
    :type actor_id: str
    :returns: plot data of chart
    :rtype: dict
    """
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

    path = movie_rating_per_year_path.format(id=actor_id)
    if not os.path.isfile(path):
        df.plot(kind='line', ax=ax, y='rating', label=actor, color='#f6c800')
        plt.title("Average movie rating per year")
        plt.savefig(path)
    path = movie_rating_compared.format(id=actor_id)
    if not os.path.isfile(path):
        plt.title("Average rating compared to other actors")
        df.plot(kind='line', ax=ax, y='avg_rating', label="all actors", color='#343A40')
        plt.savefig(path)
    plt.close()
    return avg_rating_dict
