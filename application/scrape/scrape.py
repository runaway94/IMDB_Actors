"""scrape.py

This script allows the user to scrape all actors, movies and awards
from the imdb top actors list.

It then stores the values in a database.

"""
import json

from IMDB_Actors.application.scrape.scrape_actor_details import Actor
from IMDB_Actors.application.scrape.scrape_helper import find_soup_from_url, print_progress_bar
from IMDB_Actors.data.save_to_database import persist_information

URL = "https://www.imdb.com/list/ls053501318/"
soup = find_soup_from_url(URL)
all_actors = soup.find('script', attrs={'type': 'application/ld+json'})
actor_objects = json.loads(all_actors.string)['about']['itemListElement']

print_progress_bar(0)
for i, actor in enumerate(actor_objects):
    actor_id = actor['url'].replace("/name/", "")[:-1]
    actor_pos = actor['position']

    # Scrape information
    actor = Actor(actor_id, actor_pos)

    # save in database
    persist_information(actor)

    # Update Progress Bar
    print_progress_bar(i + 1)

print("scraping complete!")
