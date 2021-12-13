import requests
from bs4 import BeautifulSoup as bs
from pprint import pprint

def cities():
    # connection
    url = 'https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=2&xnumnuts=2103'
    r = requests.get(url)
    soup = bs(r.text, "html.parser")

    # get urls of all cities
    links = []
    for a in soup.find_all('a', href=True):
        if "vyber" in a['href']:
            links.append('https://volby.cz/pls/ps2017nss/' + a['href'])
        else:
            continue

    format_links = set(links)
    return list(format_links)


pprint(cities())