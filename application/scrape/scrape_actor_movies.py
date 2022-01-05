import re

from IMDB_Actors.application.scrape.scrape_helper import find_soup_from_url, wrap_and_escape_text

actress_url = "https://www.imdb.com/filmosearch/?role={id}&sort=moviemeter," \
              "asc&job_type=actress&title_type=movie&title_type=short&title_type=musicVideo&title_type=video" \
              "&title_type=tvMovie "
actor_url = "https://www.imdb.com/filmosearch/?role={id}&sort=moviemeter," \
            "asc&job_type=actor&title_type=movie&title_type=short&title_type=musicVideo&title_type=video&title_type" \
            "=tvMovie "


class Movie:
    def __init__(self, actor_id, movie_entry):
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
        return {
            "movieID": self.movieID,
            "title": self.title,
            "year": self.year,
            "runtime": self.runtime,
            "rating": self.rating
        }

    def get_genres(self):
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
    if gender == "'female'":
        url = actress_url.format(id=actor_id)
    else:
        url = actor_url.format(id=actor_id)
    movie_list = scrape_movie_from_url(url, [], actor_id)
    return movie_list


def scrape_movie_from_url(URL, movie_list, actor):
    soap = find_soup_from_url(URL)
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
    genre_findings = movie_entry.find(attrs={'class': 'genre'})
    if genre_findings is None:
        return ""
    return genre_findings.get_text().strip().split(',')


def find_rating(movie_entry):
    rating_finding = movie_entry.find(attrs={'class': 'ratings-imdb-rating'})
    if rating_finding is None:
        return 0
    return rating_finding.find('strong').get_text()


def find_runtime(movie_entry):
    runtime_finding = movie_entry.find(attrs={'class': 'runtime'})
    if runtime_finding is None:
        return 0
    return runtime_finding.get_text().replace("min", "").replace(".", "")

