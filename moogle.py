import pickle
import requests
import urllib3
import sys
import util
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from bs4.element import Comment
from networkx import graph

from stop_words import get_stop_words
from langdetect import detect
from langdetect import detect_langs

from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

sys.setrecursionlimit(50000)

f = open("noise.txt")
NOISE = list(f.read().split(','))

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
    try:
        lang = detect(text)
    except:
        lang = 'en'
        
    stop_words = get_stop_words(lang)
    text = text.split(' ')
    return [word for word in text if word not in stop_words]
    # Sanitize Text


def is_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True


def filterVisibleText(text):
    visible = filter(is_visible, text)
    return u" ".join(t.strip() for t in visible)


def getText(soup):
    text = filterVisibleText(soup.findAll(text=True)) 
    text = sanitizeText(text)
    return set(text)



def scrapeSite(soup, url, db):
    words = db["words"]
    text = getText(soup)
    for word in text:
        if word not in words:
            words[word] = set([url])
        else:
            words[word].add(url)

    db["words"] = words


def sanitizeUrl(parent_url, url):
    if "http" not in url:
        url = urljoin(parent_url, url)
    return url


def getSoup(url):
    # Returns HTML (text) of the given URL.
    response = requests.get(url, verify=False).text
    # Creates 'soup' object from response (HTML). 'soup' is a python object that contains all the content and information/metadata of the website.
    soup = BeautifulSoup(response)
    return soup


def getLinks(soup):
    links = []
    for link in soup.find_all('a'):
        href = link.get("href")
        if href != None and 'mailto:' not in href:
            links.append(href)
    return links


def recursive_crawler(url, expdist, db, G):
    pages = db["pages"]
    if expdist >= 0:
        if url not in pages:
            soup = getSoup(url)
            #pages[url] = enllaços que apunta no soup
            pages[url] = soup
            scrapeSite(soup, url, db)
        if expdist > 0:
            links = getLinks(pages[url])  
            # add node u 
            G.add
            for link in links:
                print(link)
                link = sanitizeUrl(url,link)
                # add node v_i
                # add edge between u an v_i
                recursive_crawler(link,expdist - 1, db)

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
    G = Graph([])
    recursive_crawler(url, maxdist, db,G)
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
    print(words)
    query_results = list(words[query])

    web_results = []
    i = 0
    for url in query_results:
        # Accedeixo al valor del diccionari que pertany a la clau url
        soup = pages[url]
        web_results.append({  # Fem un append d'un diccionari a la llista pages
            'url': url,  # URL : URL
            'title': soup.title.string,
            'score': 100 - i
        })
        i += 1

    return web_results
