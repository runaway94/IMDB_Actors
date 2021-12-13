import json

from IMDB_Actors.application.scrape.scrape_actor_awards import scrape_award
from IMDB_Actors.application.scrape.scrape_actor_details import scrape_actor
from IMDB_Actors.application.scrape.scrape_actor_movies import scrape_movie
from IMDB_Actors.application.scrape.scrape_helper import find_soup_from_url
from IMDB_Actors.data.save_to_database import save_actor, save_awards, save_movie

URL = "https://www.imdb.com/list/ls053501318/"

soup = find_soup_from_url(URL)

all_actors = soup.find('script', attrs={'type': 'application/ld+json'})
strip = str(all_actors)[35:-9]

data = json.loads(str(strip))
all_actors = data['about']['itemListElement']
counter = 0
for actor in all_actors:

    counter = counter + 1
    print("Scraping actor number " + str(counter) + " of 50 . . .")

    actor_id = actor['url'].replace("/name/", "")[:-1]
    actor = scrape_actor(actor_id)
    awards = scrape_award(actor_id)
    movies = scrape_movie(actor_id, actor['gender'])

    save_actor(actor)
    for award in awards:
        save_awards(award)
    for movie in movies:
        save_movie(movie)

