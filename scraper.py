import requests
import csv
import os
from bs4 import BeautifulSoup as bs


# stáhnout html výsledky každého města včetně volených stran
# naformatovat do slovniku?
# uloz do csv - headers
#
def main():
    format_respond_city = get_html_city()
    table_results_city = data_table(format_respond_city)
    votes_data = get_votes_data(table_results_city)

    format_respond_district = get_html_district()
    table_results_district = data_table(format_respond_district)
    location_data = get_location_data(table_results_district)
    print(location_data)





def get_html_district():
    url = "https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=2&xnumnuts=2103"
    r = requests.get(url)
    format_r = bs(r.text, "html.parser")
    return format_r


def get_html_city():  # udělat loop pro každou obec
    url = f"https://volby.cz/pls/ps2017nss/ps311?xjazyk=CZ&xkraj=2&xobec=535010&xvyber=2103"
    r = requests.get(url)
    format_r = bs(r.text, "html.parser")
    return format_r


def data_table(respond):  # tabulka kde jsou uložená data voliči v seznamu, vydané obálky, platné hlasy
    return respond.find("table", {"class": "table"})


def get_votes_data(table):  # potřebuju přidat obec, kód obce asi od jinud, volené strany
    registered = table.find("td",
                           {"class": "cislo", "data-rel": "L1", "headers": "sa2"}
                           ).text
    envelopes = table.find("td",
                           {"class": "cislo", "data-rel": "L1", "headers": "sa3"}
                           ).text
    valid = table.find("td",
                       {"class": "cislo", "data-rel": "L1", "headers": "sa6"}
                       ).text

    return {"registered": registered, "envelopes": envelopes, "valid": valid}


def get_location_data(table):
    code = table.find("td",
                        {"class": "cislo", "headers": "t1sa1 t1sb1"}
                        ).text
    location = table.find("td",
                          {"class": "overflow_name", "headers": "t1sa1 t1sb2"}
                        ).text

    return {"code": code, "location": location}


if __name__ == "__main__":
    main()
