from bs4 import BeautifulSoup as soup
from urllib.request import Request, urlopen
import re
import time


def scrape_prices_from_page_num(
    page_num,
):  # scrapes prices and names from page of given number
    page_url = (
        f"https://www.futwiz.com/en/fifa23/players?page={page_num}&release=nifgold"
    )
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

    # print(prices)

    data_name = bs.findAll("td", {"class": "ovr"})

    links = []

    for item in range(len(data_name)):
        # print(data_name[item].findChild('a'))

        string = str(data_name[item].findChild("a"))
        # print(''.join(string.splitlines()))
        rstring = re.compile(r"\/en\/fifa23\/player\/\S*[-]?[a-zA-Z'-]+\/\d{2,}")
        regex = rstring.findall(string)
        if regex:
            links.append(regex[0])

    # print(links)

    dictionary_links_values_one_page = {}
    for key in links:
        for value in prices:
            dictionary_links_values_one_page[key] = value
            prices.remove(value)
            break

    # print(dictionary_links_values_one_page)
    return dictionary_links_values_one_page, links


def scrape_prices_from_pages(
    pages,
):  # concatenates dictionaries od link: price pairs and a list of links
    dictionary_links_values = {}
    links_list = []
    for num in range(pages):
        print("SCRAPING FROM PAGE ", num)
        dictionary_links_values_one_page, links = scrape_prices_from_page_num(num)
        dictionary_links_values.update(dictionary_links_values_one_page)
        if links_list is None:
            links_list = list
        else:
            links_list = links_list + links
        # print(links_list)
        # print(dictionary_links_values)
        time.sleep(5)
    print(dictionary_links_values)

    return dictionary_links_values, links_list


# dictionary_links_values_one_page, links =scrape_prices_from_page_num(5)
# dictionary_links_values, links_list = scrape_prices_from_pages(3)
# print(dictionary_links_values)


def find_player_by_name(
    dictionary_links_values, links_list, *names
):  # finds players link and price by name
    # print(names)
    found_links = []
    found_values = []
    for name in names:
        # print(name, type(name))
        if name is None:
            return found_links, found_values
        name = name.lower()

        link = list(filter(lambda x: name in x, links_list))
        value = [
            value
            for key, value in dictionary_links_values.items()
            if name in key.lower()
        ]
        # print(link, type(link))
        # print(value, type(value))

        if len(link) is not 0:
            found_links.append(link[0])

        if len(value) is not 0:
            found_values.append(value[0])

        # found_links = list(filter(lambda x: name in x, links_list))
        # print(found_links)
        # found_values = [
        #    value for key, value in dictionary_links_values.items() if name in key.lower()
        # ]
        # print(found_values)
    return found_links, found_values


#
# dic, links = scrape_prices_from_pages(10)
##print(dic)
##print(len(dic), len(links))
# run = True
# names = []
# while run == True:
#    name = input()
#    if name == 'q':
#        run = False
#    elif name == 's':
#        for i in range(len(names)):
#            find_player_by_name(dic, links, names[i])
#        names.clear()
#    else:
#        names.append(name)
#
