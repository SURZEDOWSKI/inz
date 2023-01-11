from bs4 import BeautifulSoup as soup
from urllib.request import Request, urlopen
import re
import time


def scrape_prices_from_page_num(
    page_num, sort
):  # scrapes prices and names from page of given number
    if sort == 1:
        page_url = (
            f"https://www.futwiz.com/en/fifa23/players?page={page_num}&release=nifgold"
        )
    elif sort == 2:
        page_url = f"https://www.futwiz.com/en/fifa23/players?page={page_num}&release=nifgold&order=bin&s=desc"

    req = Request(url=page_url, headers={"User-Agent": "Mozilla/5.0"})
    webpage = urlopen(req).read()

    bs = soup(webpage, "html.parser")

    data_price = bs.findAll("td", {"width": "30"})

    prices = []

    for item in range(len(data_price)):
        string = str(data_price[item])
        regex = re.findall(
            r"\d*\.?\d*[K]|\d\d\d", string
        )  # checks for price ending with "K", can include ".", or for 3 digits in a row
        if regex:
            prices.append(regex[0])

    data_name = bs.findAll("td", {"class": "ovr"})

    links = []

    for item in range(len(data_name)):

        string = str(data_name[item].findChild("a"))

        rstring = re.compile(r"\/en\/fifa23\/player\/\S*[-]?[a-zA-Z'-]+\/\d{2,}")
        regex = rstring.findall(string)
        if regex:
            links.append(regex[0])

    dictionary_links_values_one_page = {}
    for key in links:
        for value in prices:
            dictionary_links_values_one_page[key] = value
            prices.remove(value)
            break

    return dictionary_links_values_one_page, links


def scrape_prices_from_pages(
    pages, sort
):  # concatenates dictionaries od link: price pairs and a list of links
    dictionary_links_values = {}
    links_list = []
    for num in range(pages):
        print("SCRAPING FROM PAGE ", num)
        dictionary_links_values_one_page, links = scrape_prices_from_page_num(num, sort)
        dictionary_links_values.update(dictionary_links_values_one_page)
        if links_list is None:
            links_list = list
        else:
            links_list = links_list + links

        time.sleep(5)
    print(dictionary_links_values)

    return dictionary_links_values, links_list


def find_player_by_name(
    dictionary_links_values, links_list, *names
):  # finds players link and price by name

    found_links = []
    found_values = []
    for name in names:

        if name is None:
            continue
        name = name.lower()

        link = list(filter(lambda x: name in x, links_list))
        value = [
            value
            for key, value in dictionary_links_values.items()
            if name in key.lower()
        ]

        if len(link) != 0:
            for i in range(len(link)):
                found_links.append(link[i])

        if len(value) != 0:
            for i in range(len(value)):
                found_values.append(value[i])

    return found_links, found_values
