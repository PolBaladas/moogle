import pickle
import requests
import urllib3
import sys
import util
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import networkx as nx
from networkx import DiGraph, pagerank
import pylab as plt
from collections import deque


from stop_words import get_stop_words

from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

sys.setrecursionlimit(50000)

STOP_WORDS = set(get_stop_words('en') +
                 get_stop_words('ca') + get_stop_words('es'))

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
    try:
        text = util.clean_words(text)
    except:
        text.encode('utf-8')
    
    text = text.split(' ')
    filter(None, text)
    return [word for word in text if word not in STOP_WORDS]


def isVisible(element):
    return element.parent.name not in [
        'style', 'script', 'head', 'title', '[document]'
    ]


def filterVisibleText(text):
    visible = filter(isVisible, text)
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
    return urljoin(parent_url, url).strip('/')


def getSoup(url):
    # Returns HTML (text) of the given URL.
    try:
        response = requests.get(url, verify=False, timeout=1)
        response_status = response.status_code == 200
        response_type = response.headers.get('content-type')
        good_response = response.status_code and 'html' in response_type
        return BeautifulSoup(response.text) if good_response else None
    except:
        print("Error: Bad Content. Skipping link and crawling on.")
        return None

    # Creates 'soup' object from response (HTML). 'soup' is a python object that contains all the content and information/metadata of the website.


def getLinks(soup):
    links = []
    for link in soup.find_all('a', href=True):
        href = link.get("href")
        if href != None and 'mailto:' not in href:
            links.append(href)
    return links


def addSite(soup, url):
    return {
        'url': url,
        'title': soup.title,
        'description': getDescription(soup),
        'score': 0
    }


def BFS_crawler(url, expdist, db, G):
    links_queue = deque()
    links_queue.appendleft([expdist, url])
    visit = set()
    while len(links_queue):
        web = links_queue.pop()
        url = web[1]
        dist = web[0]
        soup = getSoup(url)
        if soup:
            db['pages'][url] = addSite(soup, url)
            scrapeSite(soup, url, db)
            if dist > 0:
                links = getLinks(soup)
                for link in links:
                    link = sanitizeUrl(url, link)
                    G.add_edge(url, link)
                    if not link in visit:
                        visit.add(link)
                        print(link)
                        links_queue.appendleft([dist-1, link])


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
    BFS_crawler(url, maxdist, db, G)
    #nx.draw(G, with_labels=True)
    #plt.plot()
    pr = pagerank(G)
    for element in pr.keys():
        try:
            db["pages"][element]['score'] = pr[element] * 100
        except :
            pass
    print(db["pages"])
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
        else:
            results.append(set())

    if not len(results):
        return results

    result_set = results[0].intersection(*results)
    print(result_set)

    web_results = []
    for url in result_set:
        web_results.append(db["pages"][url])

    return web_results