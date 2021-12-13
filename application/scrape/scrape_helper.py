import requests
from bs4 import BeautifulSoup


def find_soup_from_url(URL):
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    return soup

def wrap_and_escape_text(text):
    text = text.replace("'", "''")
    text = BeautifulSoup(text, "lxml").text
    text = "\'" + text + "\'"
    return text
