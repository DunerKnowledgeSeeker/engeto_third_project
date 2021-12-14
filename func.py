import requests
from bs4 import BeautifulSoup as bs
from pprint import pprint

# maybe import sys for sys.argv - according to tak

url = 'https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=2&xnumnuts=2103'
test_url= "https://volby.cz/pls/ps2017nss/ps311?xjazyk=CZ&xkraj=2&xobec=532908&xvyber=2103"


def main():
    cities_links = get_cities_url(url)
    location_codes_list = get_location_code(url)



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


def get_vote_data(city_url):
    try:
        r = requests.get(city_url)
    except requests.exceptions.HTTPError as err:
        raise exit(err)
    soup = bs(r.text, "html.parser")

    # get location
    location = soup.find_all({"h3"})[2]
    format_name = location.text.split(":")
    location_name = format_name[1].strip(" \n")

    # get registered, envelopes, valid
    registered = soup.find("td", {"class": "cislo", "headers": "sa2", "data-rel": "L1"})
    envelopes = soup.find("td", {"class": "cislo", "headers": "sa3", "data-rel": "L1"})
    valid = soup.find("td", {"class": "cislo", "headers": "sa6", "data-rel": "L1"})

    # get political parties -> dict - key = name, value = number of votes
    parties_names = []
    parties_votes = []
    for name in soup.find_all("td", {"class": "overflow_name", "headers": "t2sa1 t2sb2"}):
        parties_names.append(name.text)
    for vote in soup.find_all("td", {"class": "cislo", "headers": "t2sa2 t2sb3"}):
        parties_votes.append(vote.text)
    print(parties_votes)
    print(parties_names)


    return location_name, registered.text, envelopes.text, valid.text
get_vote_data(test_url)


# get political parties = HEADERS
# create generator with get_vote_data func - arguments = list(url)
# add location code to csv = extra function
# from func get_code_data and get_vote_data = create csv
# save to csv

if __name__ == '__main__':
    main()