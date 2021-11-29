import json

import requests
from bs4 import BeautifulSoup

from IMDB_Actors.application.scrape.scrape_from_actor import scrape_actor, scrape_award, scrape_movie
from IMDB_Actors.data.save_to_database import save_actor, save_awards, save_movie

URL = "https://www.imdb.com/list/ls053501318/"
page = requests.get(URL)

soup = BeautifulSoup(page.content, "html.parser")

all_actors = soup.find('script', attrs={'type': 'application/ld+json'})
strip = str(all_actors)[35:-9]

data = json.loads(str(strip))
all_actors = data['about']['itemListElement']
counter = 0
for actor in all_actors:
    counter = counter + 1
    print("Scraping actor number " + str(counter) + " of 50 . . .")
    id = actor['url'].replace("/name/", "")[:-1]
    actor = scrape_actor(id, counter)
    awards = scrape_award(id)
    movies = scrape_movie(id)
    del movies[-1]

    save_actor(actor)
    for award in awards:
        save_awards(award)
    for movie in movies:
        save_movie(movie)
