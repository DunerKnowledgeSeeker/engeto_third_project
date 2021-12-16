import requests
from bs4 import BeautifulSoup as bs


def get_cities_url(district_url):
    """Create a list of urls of all cities in chosen district"""
    try:
        r = requests.get(district_url)
        print(f"DOWNLOADING DATA FROM SELECTED URL:  {district_url}")
    except requests.exceptions.HTTPError as err:
        raise exit(err)
    soup = bs(r.text, "html.parser")

    links = []
    for a in soup.find_all('a', href=True):
        if "vyber" in a['href']:
            links.append('https://volby.cz/pls/ps2017nss/' + a['href'])
        else:
            continue
    format_links = list(dict.fromkeys(links))

    return format_links


def get_location_code(district_url):
    """Create a dictionary that contains cities codes as keys and cities names as values"""
    try:
        r = requests.get(district_url)
    except requests.exceptions.HTTPError as err:
        raise exit(err)
    soup = bs(r.text, "html.parser")
    codes = [code.text for code in soup.find_all("td", {"class": "cislo"})]
    locations = [location.text for location in soup.find_all("td", {"class": "overflow_name"})]
    sorted_codes_locations = zip(codes, locations)

    return dict(sorted_codes_locations)


def get_vote_data(city_url):
    """
    Scrape needed data from city_url to get results of elections
    registered voters, submitted, envelopes, verified votes
    dictionary with contains key = name of the city, value = number of votes
    """
    try:
        r = requests.get(city_url)
    except requests.exceptions.HTTPError as err:
        raise exit(err)
    soup = bs(r.text, "html.parser")

    # get registered, envelopes, valid
    registered = soup.find("td", {"class": "cislo", "headers": "sa2", "data-rel": "L1"})
    envelopes = soup.find("td", {"class": "cislo", "headers": "sa3", "data-rel": "L1"})
    valid = soup.find("td", {"class": "cislo", "headers": "sa6", "data-rel": "L1"})

    # get political parties and votes -> dict
    parties_names = [name.text for name in soup.find_all("td", {"class": "overflow_name"})]
    number_votes_table_1 = [vote.text for vote in soup.find_all("td", {"class": "cislo", "headers": "t1sa2 t1sb3"})]
    number_votes_table_2 = [vote.text for vote in soup.find_all("td", {"class": "cislo", "headers": "t2sa2 t2sb3"})]
    number_votes = number_votes_table_1 + number_votes_table_2
    politic_parties_results = zip(parties_names, number_votes)

    return {"REGISTERED": registered.text}, {"ENVELOPES": envelopes.text}, {"VALID": valid.text}, dict(
        politic_parties_results)


def get_data_all_url(district_url):
    all_url = get_cities_url(district_url)
    for data in all_url:
        registered, envelopes, valid, political_parties = get_vote_data(data)
        yield registered, envelopes, valid, political_parties
