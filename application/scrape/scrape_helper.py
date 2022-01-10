"""scrape_helper.py
--------
Library that contains functions for the scraping
"""
import sys

import requests
from bs4 import BeautifulSoup


def find_soup_from_url(url):
    """creates soup from url

    :param url: url to website
    :type url: str
    :returns: soup of website
    :rtype: BeautifulSoup
    """
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    return soup


def wrap_and_escape_text(text):
    """makes strings easier to dave in databases

    :param text: text to escape
    :type text: str
    :returns: escaped text
    :rtype: str
    """
    text = text.replace("'", "''")
    text = BeautifulSoup(text, "lxml").text
    text = "\'" + text + "\'"
    return text


def print_progress_bar(iteration):
    """Call in a loop to create terminal progress bar
    :param iteration: current iteration
    :type iteration: int
    """
    filled_length = int(100 * iteration // 50)
    bar = '█' * filled_length + '-' * (100 - filled_length)
    sys.stdout.write('\r%s |%s| %s %s' % ('Progress', bar, iteration, ' of 50 actors scraped')),
    if iteration == 50:
        print()
    sys.stdout.flush()
