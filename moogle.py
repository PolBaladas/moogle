import pickle
import requests
import urllib3
import sys
from urllib.parse import urljoin
from bs4 import BeautifulSoup

sys.setrecursionlimit(50000)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

#############################################################################
# Common part
#############################################################################


def authors():
    """Returns a string with the name of the authors of the work."""

    ### Please modify this function

    return "Oriol Domingo, Pol Baladas"



#############################################################################
# Crawler
#############################################################################

def store(db, filename):
    with open(filename, "wb") as f:
        print("store", filename)
        pickle.dump(db, f)
        print("done")


def getSoup(url):
    response = requests.get(url, verify = False).text # Returns HTML (text) of the given URL.
    soup = BeautifulSoup(response) # Creates 'soup' object from response (HTML). 'soup' is a python object that contains all the content and information/metadata of the website.
    return soup

def getLinks(soup):
    links = []
    for link in soup.find_all('a'):
        href = link.get("href")
        if href != None and 'mailto:' not in href:
            links.append(href)
    return links


def sanitizeUrl(parent_url, url):
    if "http" not in url:
        url = urljoin(parent_url, url)
    return url

def crawler(url, maxdist):
    """
        Crawls the web starting from url,
        following up to maxdist links
        and returns the built database.
    """
    db = {
        "pages": {},
        "words": {}
    }
    recursive_crawler(url, maxdist, db["pages"])
    return db["pages"]
    
def recursive_crawler(url, maxdist, pages):
    if url not in pages:
        soup = getSoup(url)
        pages[url] = soup
    if maxdist > 0 :
        links = getLinks(soup)
        for link in links:
            link = sanitizeUrl(url, link)
            recursive_crawler(link, maxdist - 1, pages)

   


#############################################################################
# Answer
#############################################################################


def load(filename):
    """Reads an object from file filename and returns it."""
    with open(filename, "rb") as f:
        print("load", filename)
        db = pickle.load(f)
        print("done")
        return db


def answer(db, query):

    """
        Returns a list of pages for the given query.

        Each page is a map with three fields:
            - title: its title
            - url: its url
            - score: its score

        The list is sorted by score in descending order.
        The query is a string of cleaned words.
    """

    pages = []
    print(len(db))
    i = 0
    for url in db:
        soup = db[url] # Accedeixo al valor del diccionari que pertany a la clau url
        pages.append({ # Fem un append d'un diccionari a la llista pages
            'url': url,  # URL : URL
            'title': soup.title.string, 
            'score': 100 - i
        })
        i+=1

    return pages

