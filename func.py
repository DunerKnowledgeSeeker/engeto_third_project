import requests
from bs4 import BeautifulSoup as bs
from pprint import pprint

# maybe import sys for sys.argv - according to tak

url = 'https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=2&xnumnuts=2103'


def main():
    cities_links = get_cities_url(url)
    print(cities_links)
    location_codes_list = get_location_code(url)
    print(location_codes_list)



def get_cities_url(district_url):
    # connection
    try:
        r = requests.get(district_url)
        print(f"DOWNLOADING DATA FROM SELECTED URL:  {district_url}")
    except requests.exceptions.HTTPError as err:
        raise exit(err)
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


def get_location_code(district_url):
    try:
        r = requests.get(district_url)
    except requests.exceptions.HTTPError as err:
        raise exit(err)
    soup = bs(r.text, "html.parser")
    codes = []
    for code in soup.find_all("td", {"class": "cislo"}):
        codes.append(code.text)

    return codes


# get data from links
    # get location
    # get registred, envelopes, valid + political parties = HEADERS
# save to csv

if __name__ == '__main__':
    main()