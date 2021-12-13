import json

from IMDB_Actors.application.scrape.scrape_helper import find_soup_from_url, wrap_and_escape_text


def scrape_actor(actor_id):
    actor = {
        "actorID": "\'" + actor_id + "\'"
    }
    scrape_actor_information("https://www.imdb.com/name/{id}".format(id=actor_id), actor)
    scrape_actor_bio("https://www.imdb.com/name/{id}/bio".format(id=actor_id), actor)
    return actor


def scrape_actor_information(actor_url, actor):
    soup = find_soup_from_url(actor_url)

    #find details of actor
    actor_detail = soup.find('script', attrs={'type': 'application/ld+json'})

    #make json readable
    strip = str(actor_detail)[35:-9]
    data = json.loads(str(strip))

    #find gender
    actor_gender = soup.find(attrs={'id': 'jumpto'}).find_all('a')
    ref = actor_gender[0]['href']
    gender = 'female'
    if "actress" not in ref:
        gender = 'male'

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


