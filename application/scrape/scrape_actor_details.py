"""scrape_actor_details.py
--------
"""
import json

from IMDB_Actors.application.scrape.scrape_actor_awards import scrape_all_awards_of_actor
from IMDB_Actors.application.scrape.scrape_actor_movies import scrape_all_movies_of_actor
from IMDB_Actors.application.scrape.scrape_helper import find_soup_from_url, wrap_and_escape_text
from IMDB_Actors.constants import actor_detail_url, actor_bio_url


class Actor:
    """Scrapes all important information of an actor"""
    def __init__(self, actor_id, pos):
        """Scrapes all important information of an actor

        :param actor_id: id of actor the movies are scraped of
        :type actor_id: str
        :param pos: position of actor
        :type pos: int
        """
        self.actorID = actor_id
        self.pos = pos
        self.scrape_actor_information()
        self.scrape_actor_bio()
        self.scrape_awards()
        self.scrape_movies()

    def scrape_actor_information(self):
        """Scrapes all important information of an actor
        """
        actor_url = actor_detail_url.format(actorID=self.actorID)
        soup = find_soup_from_url(actor_url)

        # find details of actor
        actor_detail = soup.find('script', attrs={'type': 'application/ld+json'})
        data = json.loads(actor_detail.string)

        # find gender
        actor_gender = soup.find(attrs={'id': 'jumpto'}).find_all('a')
        gender = 'male'
        for g in actor_gender:
            ref = g['href']
            if "actress" in ref:
                gender = 'female'

        # update new information
        self.__setattr__("name", wrap_and_escape_text(data['name']))
        self.__setattr__("birthdate", "\'" + data['birthDate'] + "\'")
        self.__setattr__("image", "\'" + data['image'] + "\'")
        self.__setattr__("gender", "\'" + gender + "\'")

    def scrape_actor_bio(self):
        """Scrapes bio of actor
        """
        url = actor_bio_url.format(actorID=self.actorID)
        soup = find_soup_from_url(url)
        bio = soup.find(attrs={'class': 'soda odd'}).find('p')
        self.__setattr__("bio", wrap_and_escape_text(str(bio)))

    def scrape_awards(self):
        """Scrapes awards of actor
        """
        awards = scrape_all_awards_of_actor(self.actorID)
        self.__setattr__("awards", awards[1:])

    def scrape_movies(self):
        """Scrapes movies of actor
        """
        movies = scrape_all_movies_of_actor(self.actorID, self.gender)
        self.__setattr__("movies", movies)

    def get_actor_information(self):
        """returns data to save in database

        :returns: data to save in database
        :rtype: dict
        """
        return {
            "actorID": "\'" + self.actorID + "\'",
            "name": self.name,
            "pos": self.pos,
            "birthdate": self.birthdate,
            "image": self.image,
            "bio": self.bio,
            "gender": self.gender
        }