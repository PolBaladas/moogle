import sys
import util
import math
import pickle
import urllib3
import requests
import operator
import pylab as plt
import networkx as nx

from bs4 import BeautifulSoup
from collections import deque
from stop_words import get_stop_words
from networkx import DiGraph, pagerank
from urllib.parse import urljoin, urlparse, urldefrag
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

sys.setrecursionlimit(50000) # Uncomment if your system needs this.

STOP_WORDS = set(get_stop_words('en') +
                 get_stop_words('ca') + get_stop_words('es'))


DOMAIN = ''
BASE = ''



#############################################################################
# Common part
#############################################################################


def authors():
    """Returns a string with the name of the authors of the work."""
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
    try:
        text = util.clean_words(text)
    except:
        text.encode('utf-8')

    text = text.split(' ')
    filter(None, text)
    return [word for word in text if word not in STOP_WORDS]


def isVisible(element):                                             # Boolean Function that will be used to filter visible text.
    return element.parent.name not in [
        'style', 'script', 'head', '[document]'
    ]


def filterVisibleText(text):
    visible = filter(isVisible, text)                               # Pass isVisible filter through text.
    return u" ".join(t.strip() for t in visible)                    # Join results in string.


def getText(soup):
    text = filterVisibleText(soup.findAll(text=True))
    text = sanitizeText(text)
    return set(text)                                                # Repeated instances are removed.


def scrapeSite(soup, url, db):
    text = getText(soup)
    for word in text:
        if word not in db['words']:
            db['words'][word] = set([url])
        else:
            db['words'][word].add(url)


def sanitizeUrl(url):
    return urljoin(BASE, url).strip('/') 


def getSoup(url):                                                   # Try/Catch block to prevent Bad Content being processed.
    try:
        response = requests.get(url, verify=False, timeout=0.5)     # As an alternative design option, one could check for the content type of the response. 
        return BeautifulSoup(response.text, 'lxml')                 # e.g: this would only work if the content type was 'text/html'.
    except:
        print("Error: Bad Content, skipping link. Do not stop.")
        return None                                                 # Return None if the URL could not be processed. The Crawler will understand.


def getDomain(url):
    return urlparse(url).netloc                                     # netloc --> Network Location means domain.


def isFromDomain(url):
    domain = getDomain(url)
    return (url[0:4] != 'http') or (domain == DOMAIN)               # Check (1) absolute/relative paths and  (2) domain procedence.


def isValidUrl(url):                                                # Boolean function that will be used to filter valid URLs.
    return (                                                        # If the conditions need to be changed, modify this function.
        "mailto:" not in url['href'] and
        '#' not in url['href'] and
        isFromDomain(url['href'])
    )


def getLinks(soup):
    results = []
    links = filter(isValidUrl, soup.find_all('a', href=True))       # Pass isValidURL filter through 'a' tags.
    for link in list(links):
        url = sanitizeUrl(link['href'])                             # Sanitize the URL format-wise.
        results.append(url)
    return results


def addSite(soup, url):
    return {
        'url': url,
        'title': soup.title.string if soup.title else 'No title',   # Strangely enough, some websites have no title tag or it is found to be empty.
        'score': 0
    }


def BFS_crawler(url, expdist, db, G):
    links_queue = deque()
    links_queue.appendleft([expdist, url])
    visit = set()
    while len(links_queue):
        dist, url = links_queue.pop()
        soup = getSoup(url)
        if soup:
            db['pages'][url] = addSite(soup, url)
            scrapeSite(soup, url, db)
            if dist > 0:
                links = getLinks(soup)
                for link in links:
                    G.add_edge(url, link)
                    if not link in visit:
                        visit.add(link)
                        print(link)
                        links_queue.appendleft([dist-1, link])
        else:
            db['pages'][url] = {}


def plotGraph(G):
    nx.draw(G, with_labels=True)
    plt.plot()
    plt.show()


def pageRank(G, db):                                                
    pr = pagerank(G)
    for element in pr.keys():
        score = math.ceil(pr[element] * 10000)                      # Ceil the PageRank score for    
        db['pages'][element]['score'] = score


def crawler(url, maxdist):
    """
        Crawls the web starting from url,
        following up to maxdist links
        and returns the built database.
    """
    global DOMAIN
    global BASE

    DOMAIN = getDomain(url)
    BASE = url

    db = {
        "pages": {},
        "words": {}
    }

    G = DiGraph([])

    print("Crawling", url)
    BFS_crawler(url, maxdist, db, G)

    print("Computing PageRank...")
    pageRank(G, db)

    print("Plotting BFS...")
    plotGraph(G)

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

    result_set = results[0].intersection(*results)                      # Calculates the intersection of result sets (queries).

    web_results = []
    for url in result_set:
        web_results.append(db["pages"][url])                            # Fill list to be returned. 

    web_results.sort(key=operator.itemgetter('score'), reverse=True)

    return web_results
