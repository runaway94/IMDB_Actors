import json
import re

import requests
from bs4 import BeautifulSoup


def scrape_actor(id, position):
    actor = {
        "pos": position,
        "actorID": "\'" + id + "\'"
    }
    scrape_actor_information("https://www.imdb.com/name/{id}".format(id=id), actor)
    scrape_actor_bio("https://www.imdb.com/name/{id}/bio".format(id=id), actor)
    return actor


def find_soup_from_url(URL):
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    return soup


def scrape_actor_information(actor_url, actor):
    soup = find_soup_from_url(actor_url)
    actor_detail = soup.find('script', attrs={'type': 'application/ld+json'})
    strip = str(actor_detail)[35:-9]
    data = json.loads(str(strip))
    # name, id, image, birthdate
    actor.update({
        "name": "\'" + data['name'] + "\'",
        "birthdate": "\'" + data['birthDate'] + "\'",
        "image": "\'" + data['image'] + "\'"
    })
    return actor


def scrape_actor_bio(actor_bio_url, actor):
    soup = find_soup_from_url(actor_bio_url)
    bio = soup.find(attrs={'class': 'soda odd'})
    bio = bio.find('p')
    bio = str(bio)[3:-4].strip()
    # bio = repr(bio)
    actor.update({
        "bio": wrap_and_escape_text(bio),
    })

    return actor


def wrap_and_escape_text(text):
    # escape single qutes
    text = text.replace("'", "''")
    text = "\'" + text + "\'"
    return text


def scrape_award(id):
    url = "https://www.imdb.com/name/{id}/awards?ref_=nm_ql_2".format(id=id)
    soup = find_soup_from_url(url)
    award_list = []
    # print(soup)
    award_names = soup.find(attrs={'class': 'article listo'}).findAll('h3')
    # print(award_names)

    name_counter = 1
    award_tables = soup.findAll('table', attrs={'class': 'awards'})

    for table in award_tables:
        header = award_names[name_counter].get_text()
        awards = table.findAll('tr')
        name_counter = name_counter + 1
        for awardEntry in awards:
            scrape_single_award(awardEntry, id, award_list, header)

    return award_list


def scrape_single_award(award_entry, actor, awardlist, title):
    found_year = award_entry.find('td', attrs={'class': 'award_year'})
    if found_year is not None:
        year = found_year.get_text().strip()
    else:
        if len(awardlist) > 0:
            year = awardlist[-1]["year"]

    found_outcome = award_entry.find('td', attrs={'class': 'award_outcome'})
    if found_outcome is not None:
        out = found_outcome.find('b').get_text().strip()
        if out == "Winner":
            outcome = 1
        else:
            outcome = 0
    else:
        if len(awardlist) > 0:
            outcome = awardlist[-1]["outcome"]

    found_category = award_entry.find(attrs={'class': 'award_category'})
    if found_category is not None:
        category = wrap_and_escape_text(found_category.get_text().strip())
    else:
        if len(awardlist) > 0:
            category = awardlist[-1]["category"]

    found_desc = award_entry.find(attrs={'class': 'award_description'})
    if found_desc is not None:
        desc = wrap_and_escape_text(found_desc.get_text().strip())
    else:
        if len(awardlist) > 0:
            desc = awardlist[-1]["description"]

    award = {
        "title": wrap_and_escape_text(title),
        "actor": wrap_and_escape_text(actor),
        "year": year,
        "outcome": outcome,
        "category": category,
        "description": desc
    }

    awardlist.append(award)
    return award

def scrape_movie_from_url(URL, movie_list, actor):
    soap = find_soup_from_url(URL)
    movies = soap.find(attrs={'class': 'lister-list'}).findAll(attrs={'class': 'lister-item-content'})
    for m in movies:
        movie = find_movie(m, actor)
        movie_list.append(movie)

    next = soap.find('a', attrs={'class': 'next-page'}, href=True)
    # if next is not None:
    #     print(next)
    #     URL = next['href']
    #     URL = "https://www.imdb.com/filmosearch/" + URL
    #     scrape_movie_from_url(URL, movie_list, actor)

    return movie_list


def find_movie(movie_entry, actor):
    movie = {
        "actor": wrap_and_escape_text(actor)
    }
    header = movie_entry.find('h3', attrs={'class': 'lister-item-header'}).find('a', href=True)

    #title = movie_entry.find('h3', attrs={'class': 'lister-item-header'}).find('a').get_text()
    title = header.get_text()
    id = header['href'].replace("/title/", "")[:-1]
    year = movie_entry.find('h3', attrs={'class': 'lister-item-header'}).find(attrs={'class': 'lister-item-year'}).\
        get_text()
    year = re.sub("[^0-9]", "", year)[:4]

    genre_findings = movie_entry.find(attrs={'class': 'genre'})
    if genre_findings is not None:
        genres = genre_findings.get_text().strip().split(',')
        movie.update({
            "genres": genres
        })

    rating_finding = movie_entry.find(attrs={'class': 'ratings-imdb-rating'})
    if rating_finding is not None:
        rating = rating_finding.find('strong').get_text()
        movie.update({
            "rating": rating,
        })

    runtime_finding = movie_entry.find(attrs={'class': 'runtime'})
    if runtime_finding is not None:
        runtime = runtime_finding.get_text().replace("min", "")
        movie.update({
            "runtime": runtime
        })
    movie.update({
        "movieID": wrap_and_escape_text(id),
        "title": wrap_and_escape_text(title),
        "year": year,
        "actor": wrap_and_escape_text(actor)
    })
    return movie

def scrape_movie(id):
    url = "https://www.imdb.com/filmosearch/?role={id}&sort=moviemeter,asc&job_type=actress".format(id=id)
    movie_list = []
    movie_list = scrape_movie_from_url(url, movie_list, id)
    url = "https://www.imdb.com/filmosearch/?role={id}&sort=moviemeter,asc&job_type=actor".format(id=id)
    movie_list.append(scrape_movie_from_url(url, movie_list, id))
    return movie_list


