import json

from IMDB_Actors.application.scrape.scrape_actor_awards import Award, scrape_all_awards_of_actor
from IMDB_Actors.application.scrape.scrape_actor_movies import scrape_movie
from IMDB_Actors.application.scrape.scrape_helper import find_soup_from_url, wrap_and_escape_text
from IMDB_Actors.data.save_to_database import persist_information


class Actor:
    def __init__(self, actor_id, pos):
        self.actorID = actor_id
        self.pos = pos
        self.scrape_actor_information()
        self.scrape_actor_bio()
        self.scrape_awards()
        self.scrape_movies()

    def scrape_actor_information(self):
        actor_url = f"https://www.imdb.com/name/{self.actorID}"
        soup = find_soup_from_url(actor_url)

        # find details of actor
        actor_detail = soup.find('script', attrs={'type': 'application/ld+json'})

        # make json readable
        strip = str(actor_detail)[35:-9]
        data = json.loads(str(strip))

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
        actor_bio_url = f"https://www.imdb.com/name/{self.actorID}/bio"
        soup = find_soup_from_url(actor_bio_url)
        bio = soup.find(attrs={'class': 'soda odd'}).find('p')
        self.__setattr__("bio", wrap_and_escape_text(str(bio)))

    def scrape_awards(self):
        awards = scrape_all_awards_of_actor(self.actorID)
        self.__setattr__("awards", awards[1:])

    def scrape_movies(self):
        movies = scrape_movie(self.actorID, self.gender)
        self.__setattr__("movies", movies)

    def get_actor_information(self):
        return {
            "actorID": "\'" + self.actorID + "\'",
            "name": self.name,
            "pos": self.pos,
            "birthdate": self.birthdate,
            "image": self.image,
            "bio": self.bio,
            "gender": self.gender
        }


def scrape_actor(actor_id, pos):
    actor = {
        "pos": pos,
        "actorID": "\'" + actor_id + "\'"
    }
    scrape_actor_information("https://www.imdb.com/name/{id}".format(id=actor_id), actor)
    scrape_actor_bio("https://www.imdb.com/name/{id}/bio".format(id=actor_id), actor)
    return actor


def scrape_actor_information(actor_url, actor):
    soup = find_soup_from_url(actor_url)

    # find details of actor
    actor_detail = soup.find('script', attrs={'type': 'application/ld+json'})

    # make json readable
    strip = str(actor_detail)[35:-9]
    data = json.loads(str(strip))

    # find gender
    actor_gender = soup.find(attrs={'id': 'jumpto'}).find_all('a')
    gender = 'male'
    for g in actor_gender:
        ref = g['href']
        if "actress" in ref:
            gender = 'female'

    # update new information
    actor.update({
        "name": wrap_and_escape_text(data['name']),
        "birthdate": "\'" + data['birthDate'] + "\'",
        "image": "\'" + data['image'] + "\'",
        "gender": "\'" + gender + "\'"
    })

    return actor


def scrape_actor_bio(actor_bio_url, actor):
    soup = find_soup_from_url(actor_bio_url)
    bio = soup.find(attrs={'class': 'soda odd'}).find('p')
    actor.update({
        "bio": wrap_and_escape_text(str(bio))
    })
    return actor


a = Actor("nm0000234", 7)
persist_information(a)
