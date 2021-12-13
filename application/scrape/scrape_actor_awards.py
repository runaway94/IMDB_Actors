from IMDB_Actors.application.scrape.scrape_helper import find_soup_from_url, wrap_and_escape_text

award_URL = "https://www.imdb.com/name/{id}/awards?ref_=nm_ql_2"


def scrape_award(actor_id):
    url = award_URL.format(id=actor_id)
    soup = find_soup_from_url(url)
    award_list = [{
                "title": "",
                "actor": "",
                "year": 0,
                "outcome": "",
                "category": "",
                "description": ""
            }]
    award_names = soup.find(attrs={'class': 'article listo'}).findAll('h3')
    award_names = award_names[1:]

    for award_name in award_names:
        table = award_name.find_next('table', attrs={'class': 'awards'})
        title = award_name.get_text()
        award_rows = table.findAll('tr')

        for award_entry in award_rows:
            award = {
                "title": wrap_and_escape_text(title),
                "actor": wrap_and_escape_text(actor_id),
                "year": find_year(award_entry, award_list[-1]["year"]),
                "outcome": find_outcome(award_entry, award_list[-1]["outcome"]),
                "category": find_category(award_entry, award_list[-1]["category"]),
                "description": find_description(award_entry, award_list[-1]["description"]),
            }
            award_list.append(award)

    return award_list[1:]


def find_year(award_entry, last_year):
    found_year = award_entry.find('td', attrs={'class': 'award_year'})
    if found_year is None:
        return last_year
    return found_year.get_text().strip()


def find_outcome(award_entry, last_outcome):
    found_outcome = award_entry.find('td', attrs={'class': 'award_outcome'})
    if found_outcome is None:
        return last_outcome
    return wrap_and_escape_text(found_outcome.find('b').get_text().strip())


def find_category(award_entry, last_category):
    found_category = award_entry.find(attrs={'class': 'award_category'})
    if found_category is None:
        return last_category
    return wrap_and_escape_text(found_category.get_text().strip())


def find_description(award_entry, last_description):
    found_desc = award_entry.find(attrs={'class': 'award_description'})
    if found_desc is None:
        return last_description
    return wrap_and_escape_text(found_desc.get_text()[:490].strip())

