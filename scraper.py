import requests
import csv
import os
from bs4 import BeautifulSoup as bs


# stáhnout html výsledky každého města včetně volených stran
# naformatovat do slovniku?
# uloz do csv - headers
#
def main():
    format_respond = get_html_city()
    table_results = vote_city_data_table(format_respond)
    test = get_votes_data(table_results)
    print(test)


def get_html_city():  # udělat loop pro každou obec
    url = f"https://volby.cz/pls/ps2017nss/ps311?xjazyk=CZ&xkraj=2&xobec=535010&xvyber=2103"
    r = requests.get(url)
    format_r = bs(r.text, "html.parser")
    return format_r


def vote_city_data_table(respond):  # tabulka kde jsou uložená data voliči v seznamu, vydané obálky, platné hlasy
    return respond.find("table", {"class": "table"})


def get_votes_data(table):  # potřebuju přidat obec, kód obce asi od jinud, volené strany
    registred = table.find("td",
                           {"class": "cislo", "data-rel": "L1", "headers": "sa2"}
                           ).text
    envelopes = table.find("td",
                           {"class": "cislo", "data-rel": "L1", "headers": "sa3"}
                           ).text
    valid = table.find("td",
                       {"class": "cislo", "data-rel": "L1", "headers": "sa6"}
                       ).text

    return {"registred": registred, "envelopes": envelopes, "valid": valid}




if __name__ == "__main__":
    main()
