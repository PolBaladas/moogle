import urllib.request
from bs4 import BeautifulSoup

url = "https://seleactivitat.cat"
response = urllib.request.urlopen(url)
page = response.read()
soup = BeautifulSoup(page, "html.parser")
print(soup.title.string)
print(soup.get_text())
for link in soup.find_all("a"):
    print(link.get("href"), link.string)
