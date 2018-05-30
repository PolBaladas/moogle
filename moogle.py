import pickle
import requests
import urllib3
import sys
import util
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import networkx as nx
from networkx import DiGraph
from networkx import pagerank
import pylab as plt


from stop_words import get_stop_words

from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

sys.setrecursionlimit(50000)

STOP_WORDS = set(get_stop_words('en') + get_stop_words('ca') + get_stop_words('es'))

#############################################################################
# Common part
#############################################################################


def authors():
    """Returns a string with the name of the authors of the work."""

    # Please modify this function

    return "Oriol Domingo, Pol Baladas"


#############################################################################
# Crawler
#############################################################################

def store(db, filename):
    with open(filename, "wb") as f:
        print("store", filename)
        pickle.dump(db, f)
        print("done")


def sanitizeText(text):
    # Sanitize Text
    text = util.clean_words(text)
    text = text.split(' ')
    return [word for word in text if word not in STOP_WORDS]


def is_visible(element):
    return element.parent.name not in [
        'style', 'script', 'head', 'title', '[document]'
    ]

def filterVisibleText(text):
    visible = filter(is_visible, text)
    return u" ".join(t.strip() for t in visible)


def getText(soup):
    text = filterVisibleText(soup.findAll(text=True))
    text = sanitizeText(text)
    return set(text)


def scrapeSite(soup, url, db):
    text = getText(soup)
    for word in text:
        if word not in db['words']:
            db['words'][word] = set([url])
        else:
            db['words'][word].add(url)

def getDescription(soup):
    description = soup.findAll(attrs={"name": "description"})
    return description if description != None else ' '


def sanitizeUrl(parent_url, url):
    return urljoin(parent_url, url)


def getSoup(url):
    # Returns HTML (text) of the given URL.
    try:
        response = requests.get(url, verify=False, timeout=1)
        response_status = response.status_code == 200
        response_type = response.headers.get('content-type')
        good_response = response.status_code and 'html' in response_type
        return BeautifulSoup(response.text) if good_response else None
    except:
        return None

    # Creates 'soup' object from response (HTML). 'soup' is a python object that contains all the content and information/metadata of the website.


def getLinks(soup):
    links = []
    for link in soup.find_all('a', href=True):
        href = link.get("href")
        if href != None:
            links.append(href)
    return links


def addSite(url, soup, pages):
    return {
        'title': soup.title,
        'description': getDescription(soup),
        'score': 0
    }


def recursive_crawler(url, expdist, db, G):
    #nx.draw(G, with_labels = True)
    #plt.show()
    #pages = db["pages"]
    if expdist >= 0:
        soup = None
        if  not list(G.neighbors(url)):
            soup = getSoup(url)
            if soup: 
                db[url] = addSite(url, soup, db["pages"])
                scrapeSite(soup, url, db)

        if expdist > 0:
            if soup:
                links = getLinks(soup)
            else:
                links = G.neighbors(url)

            for link in links:
                link = sanitizeUrl(url, link)
                G.add_edge(url,link)
                print(link)
                recursive_crawler(link, expdist - 1, db, G)


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
    G = DiGraph([])
    #Cas base
    G.add_node(url)
    recursive_crawler(url, maxdist, db, G)
    pr = pagerank(G)
    print(pr)
    nx.draw(G, with_labels = True)
    plt.show()
    return db


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

    words = db["words"]
    pages = db["pages"]
    queries = query.split(' ')
    results = []
    for query in queries:
        if query in words:
            results.append(words[query])

    web_results = []

    web_results = []
    for url in query_results:
        # Accedeixo al valor del diccionari que pertany a la clau url
        web_results.append()

    return web_results