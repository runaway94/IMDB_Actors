import collections
from collections import Counter

import pandas as pd
import pylab
from matplotlib import pyplot as plt
from wordcloud import WordCloud
import os.path

from IMDB_Actors.data.get_from_database import get_awards_of, get_movies_of, get_award_wins_of, get_avg_awards, \
    get_avg_amounts, get_avg_movie_rating_per_year, get_general_rating_dict, get_actor_name, get_genres_of_actor, \
    get_genres_of_top_movies

pie_chart_path = "../presentation/static/images/movie_charts/movies_piechart_{id}.png"
wordloud_path = "../presentation/static/images/movie_charts/movies_wordcloud_{id}.png"
movie_rating_path = "../presentation/static/images/movie_charts/movies_rating_per_year_{id}.png"
movie_rating_comp_path = "../presentation/static/images/movie_charts/ratings_compared_{id}.png"
award_path = "../presentation/static/images/award_charts/award_charts_{id}.png"
award_compare_path = "../presentation/static/images/award_charts/award_compare_charts_{id}.png"
general_chart_path = "../presentation/static/images/charts/charts_{id}.png"


def create_charts(movies, actorID):

    pie_path = pie_chart_path.format(id=actorID)
    create_pie_chart(movies, pie_path)
    # if not os.path.isfile(pie_path):
    #     create_pie_chart(movies, pie_path)

    # word_path = wordloud_path.format(id=actorID)
    # if not os.path.isfile(word_path):
    #     create_wordcloud(movies, word_path)

def temp(actor_id):
    genres = get_genres_of_top_movies(actor_id)
    df = pd.DataFrame(genres)
    df = df.set_index('genre')
    df.plot.pie(y='amount', autopct='%1.1f%%', legend=None)
    pylab.ylabel('')
    pie_path = pie_chart_path.format(id=actor_id)
    plt.savefig(pie_path)
    plt.close()
    return df.to_dict()['amount']

def temp2(actor_id):
    genres = get_genres_of_actor(actor_id)
    df = pd.DataFrame(genres)
    df = df.set_index('genre')
    wordcloud = WordCloud(background_color="white")
    dic = df.to_dict()['amount']
    wordcloud.generate_from_frequencies(frequencies=dic)
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    path = wordloud_path.format(id=actor_id)
    plt.savefig(path)
    plt.close()
    return dic


def create_pie_chart(movies, path):
    print(movies)
    gen_for_pie = ""
    for m in movies[:5]:
        gen_for_pie = gen_for_pie + m['genres'] + ", "
    print(gen_for_pie)
    genres = dict(Counter(gen_for_pie.split(',')))
    plt.pie(list(genres.values()), labels=genres.keys())
    plt.axis('equal')
    plt.savefig(path)
    plt.close()


def create_wordcloud(movies, path):
    genres_text = ""
    for m in movies:
        genres_text = genres_text + m['genres'] + " "

    wordcloud = WordCloud(background_color="white").generate(genres_text)
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.savefig(path)
    plt.close()


def create_awards_per_year(actor_id):
    award_wins = get_award_wins_of(actor_id)
    awards = get_awards_of(actor_id)
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


def create_awards_avg(actor_id):
    actor_wins = get_award_wins_of(actor_id)
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


def general_avg_chart(actor_id):
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


def movie_rating_per_year_p(actor_id):
    ax = plt.subplot()
    avg_rating_dict = get_avg_movie_rating_per_year(actor_id)
    df_movie_ratings = pd.DataFrame.from_dict(avg_rating_dict, orient='index')
    ax.plot(df_movie_ratings['rating'], label='average movie rating per year')
    plt.title("Average movie rating per year")
    plt.ylabel("Rating")
    plt.xlabel("Year")
    path = movie_rating_path.format(id=actor_id)
    axs = plt.gca()
    dic = get_general_rating_dict()
    df = pd.DataFrame(dic)
    df = df[df.avg_rating.notnull()]
    print(df)
    df = df.astype(float)
    df.plot(kind='line', x='year', y='avg_rating', ax=axs, label='all actors')
    plt.savefig(path)
    plt.close()
    return avg_rating_dict


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
    plt.show()
    plt.close()

    # df_movie_ratings['rating'].astype(float).plot(kind='line', ax=ax, y='rating', label="avg rating", color='#f6c800')
    # df_movie_ratings.plot(kind='line', ax=ax, y='amount', label="amount of movies", color='#343A40')
    # plt.show()
    # plt.close()
    return avg_rating_dict


#
# award_wins = get_award_wins_of("nm0000199")
# awards = get_awards_of("nm0000199")
# movies = get_movies_of("nm0000199")
# create_charts(movies, "nm0000199")
general_avg_chart( "nm0000199")
# create_awards_per_year("nm0000199")
# movie_rating_per_year("nm0000199")
# create_awards_avg("nm0000173")
# general_avg_chart("nm0000173")
# movie_rating_per_year("nm0000173")
