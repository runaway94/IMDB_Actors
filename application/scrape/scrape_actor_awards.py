"""scrape_actor_awards.py
--------
"""
import hashlib

from IMDB_Actors.application.scrape.scrape_helper import find_soup_from_url, wrap_and_escape_text
from IMDB_Actors.constants import award_URL


def find_year(award_entry, last_award):
    found_year = award_entry.find('td', attrs={'class': 'award_year'})
    if found_year is None:
        return last_award.year
    return found_year.get_text().strip()


def find_outcome(award_entry, last_award):
    found_outcome = award_entry.find('td', attrs={'class': 'award_outcome'})
    if found_outcome is None:
        return last_award.outcome
    return wrap_and_escape_text(found_outcome.find('b').get_text().strip())


def find_category(award_entry, last_award):
    found_category = award_entry.find(attrs={'class': 'award_category'})
    if found_category is None:
        return last_award.category
    return wrap_and_escape_text(found_category.get_text().strip())


def find_description(award_entry, last_award):
    found_desc = award_entry.find(attrs={'class': 'award_description'})
    if found_desc is None:
        return last_award.description
    return wrap_and_escape_text(found_desc.get_text()[:490].strip())


class Award:
    def __init__(self, title=None, award_entry=None, last_award=None):
        """Scrapes all important information from award entry

        :param title: name of the award
        :type title: str
        :param award_entry: award entry to scrape from
        :type award_entry: PageElement
        :param last_award: last added award
        :type last_award: Award
        """
        if award_entry is not None:
            self.title = title
            self.year = find_year(award_entry, last_award)
            self.outcome = find_outcome(award_entry, last_award)
            self.category = find_category(award_entry, last_award)
            self.description = find_description(award_entry, last_award)
            self.generate_key()

    def get_award_info(self):
        """returns data to save in database

        :returns: data to save in database
        :rtype: dict
        """
        return {
            "awardID": self.awardID,
            "year": self.year,
            "category": self.category,
            "title": self.title
        }

    def get_linking_information(self):
        """returns data to save in database

        :returns: data to save in database
        :rtype: dict
        """
        return {
            "awardID": self.awardID,
            "outcome": self.outcome,
            "description": self.description
        }

    def generate_key(self):
        """generates unique primary key for awards table
        """
        s = str(self.get_award_info)
        key = int(hashlib.sha1(s.encode("utf-8")).hexdigest(), 16) % (10 ** 8)
        self.__setattr__("awardID", key)


def scrape_all_awards_of_actor(actor_id):
    """Scrapes all awards of one actor
    :type actor_id: str
    :param actor_id: id of the actor the awards are to get scraped of
    :returns: list of all awards
    :rtype: list
    """
    award_url = award_URL.format(actorID=actor_id)
    soup = find_soup_from_url(award_url)
    awards = [Award()]

    award_names = soup.find(attrs={'class': 'article listo'}).findAll('h3')
    award_names = award_names[1:]

    for award_name in award_names:
        table = award_name.find_next('table', attrs={'class': 'awards'})
        title = award_name.get_text()
        award_rows = table.findAll('tr')

        for award_entry in award_rows:
            award = Award(title=wrap_and_escape_text(title), award_entry=award_entry,
                          last_award=awards[-1])
            awards.append(award)

    return awards[1:]
