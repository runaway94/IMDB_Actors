"""scrape_actor_movies.py
--------
"""
import re

from IMDB_Actors.application.scrape.scrape_helper import find_soup_from_url, wrap_and_escape_text
from IMDB_Actors.constants import actress_movies_url, actor_movie_url


class Movie:
    """Class that stores all important movie information
    """
    def __init__(self, actor_id, movie_entry):
        """Scrapes all important information from movie entry

        :param actor_id: id of actor the movies are scraped of
        :type actor_id: str
        :param movie_entry: movie entry to scrape from
        :type movie_entry: PageElement
        """
        header = movie_entry.find('h3', attrs={'class': 'lister-item-header'})
        if header is None:
            return
        header = header.findAll('a', href=True)
        title = header[0].get_text()
        movie_id = header[0]['href'].replace("/title/", "")[:-1]
        self.movieID = wrap_and_escape_text(movie_id)
        self.title = wrap_and_escape_text(title)
        self.actor = wrap_and_escape_text(actor_id)
        self.year = find_year(movie_entry)
        self.genres = find_genres(movie_entry)
        self.rating = find_rating(movie_entry)
        self.runtime = find_runtime(movie_entry)

    def get_movie_information(self):
        """returns data to save in database

        :returns: data to save in database
        :rtype: dict
        """
        return {
            "movieID": self.movieID,
            "title": self.title,
            "year": self.year,
            "runtime": self.runtime,
            "rating": self.rating
        }

    def get_genres(self):
        """returns genres of movie

        :returns: genres of movie
        :rtype: list(dict)
        """
        genre_list = []
        for genre in self.genres:
            genre = genre.strip()
            genre_list.append(
                {
                    "title": "\'" + genre + "\'",
                    "movieID": self.movieID
                }
            )
        return genre_list


def scrape_all_movies_of_actor(actor_id, gender):
    """Scrapes all movies of one actor

    :param actor_id: id of actor
    :type actor_id: str
    :param gender: gender of actor
    :type gender: str
    :returns: list of all movies
    :rtype: list of Movies
    """
    if gender == "'female'":
        url = actress_movies_url.format(actorID=actor_id)
    else:
        url = actor_movie_url.format(actorID=actor_id)
    movie_list = scrape_movie_from_url(url, [], actor_id)
    return movie_list


def scrape_movie_from_url(url, movie_list, actor):
    """Scrapes movies of one actor

    :param actor: id of actor
    :type actor: str
    :param url: url to scrape from
    :type url: str
    :param movie_list: list of movies that were already scraped
    :type movie_list: list
    :returns: list of scraped movies
    :rtype: list of Movies
    """
    soap = find_soup_from_url(url)
    movies = soap.find(attrs={'class': 'lister-list'})
    if movies is None:
        return movie_list

    movies = movies.findAll(attrs={'class': 'lister-item-content'})

    for m in movies:
        movie_list.append(Movie(actor, m))

    next_page = soap.find('a', attrs={'class': 'next-page'}, href=True)
    if next_page is not None:
        next_url = "https://www.imdb.com/filmosearch/" + next_page['href']
        scrape_movie_from_url(next_url, movie_list, actor)

    return movie_list


def find_year(movie_entry):
    """Scrape year from element

    :param movie_entry: element to scrape from
    :type movie_entry: PageElement
    :returns: year
    :rtype: int
    """
    year = movie_entry.find('h3', attrs={'class': 'lister-item-header'}).findAll(attrs={'class': 'lister-item-year'})
    if len(year) == 0:
        return 0
    if len(year) == 1:
        year = year[0]
    else:
        year = year[1]
    year = re.sub("[^0-9]", "", year.get_text())[:4]
    if year is None or len(year) < 1:
        return 0
    return year


def find_genres(movie_entry):
    """Scrape genres from element

    :param movie_entry: element to scrape from
    :type movie_entry: PageElement
    :returns: genres
    :rtype: list
    """
    genre_findings = movie_entry.find(attrs={'class': 'genre'})
    if genre_findings is None:
        return ""
    return genre_findings.get_text().strip().split(',')


def find_rating(movie_entry):
    """Scrape rating from element

    :param movie_entry: element to scrape from
    :type movie_entry: PageElement
    :returns: rating
    :rtype: str
    """
    rating_finding = movie_entry.find(attrs={'class': 'ratings-imdb-rating'})
    if rating_finding is None:
        return 0
    return rating_finding.find('strong').get_text()


def find_runtime(movie_entry):
    """Scrape runtime from element

    :param movie_entry: element to scrape from
    :type movie_entry: PageElement
    :returns: runtime
    :rtype: str
    """
    runtime_finding = movie_entry.find(attrs={'class': 'runtime'})
    if runtime_finding is None:
        return 0
    return runtime_finding.get_text().replace("min", "").replace(".", "")

