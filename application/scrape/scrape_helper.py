import sys

import requests
from bs4 import BeautifulSoup


def find_soup_from_url(URL):
    """
    Returns the soup from a URL
    """
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    return soup


def wrap_and_escape_text(text):
    """
    Escapes quotes in texts and removes html tags.
    Converts text into a format that can be stored as a string in the database.
    """
    text = text.replace("'", "''")
    text = BeautifulSoup(text, "lxml").text
    text = "\'" + text + "\'"
    return text


def print_progress_bar(iteration):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
    """
    filled_length = int(100 * iteration // 50)
    bar = '█' * filled_length + '-' * (100 - filled_length)
    sys.stdout.write('\r%s |%s| %s %s' % ('Progress', bar, iteration, ' of 50 actors scraped')),
    if iteration == 50:
        print()
    sys.stdout.flush()
