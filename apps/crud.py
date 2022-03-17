import json
import re

import requests
from bs4 import BeautifulSoup as BS


HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.1 Safari/605.1.15"
}


url = "https://www.avito.ru/moskva/nedvizhimost"
html = requests.get(url, headers=HEADERS).text
soup = BS(html, "lxml")
catalog_items = (soup.find(
    "div", {"id": "app"})).find("div", {"class": (re.search("styles-list-\w+", str(soup))).group()}).findAll("div", {"class": (re.search("styles-item-\w+", str(soup))).group()})


item = catalog_items[1]

# with open("test.txt", "a") as f:
#     f.write(str(item))

title = item.find("div", {"class": (re.search("body-titleRow-\w+", str(item))).group()}).a["title"]

price = item.find("div", {"class": (re.search("body-priceRow-\w+", str(item))).group()})
price_value = price.find("meta", {"itemprop": "price"})["content"]
price_currency = price.find("meta", {"itemprop": "priceCurrency"})["content"]
price_note = (item.find("span", {"class": (re.search("price-text-\w+\s\w+-\w+-\w+\s\w+-\w+-\w+-\w+", str(item))).group()})).contents
if len(price_note) > 4:
    price_note = price_note[-1]
else:
    price_note = None

address = item.find("div", {"class": (re.search("geo-root-\w+", str(item))).group()}).span.span.string

placement_date = item.find("span", {"class": (re.search("text-text-LurtD\s\w+-\w+-\w+-\w+\s\w+-\w+-\w+-\w+", str(item))).group()}).string

photo_url = (item.find("div", {"class": (re.search("photo-slider-item-\w+", str(item))).group()})).img["src"]

url_address = "https://www.avito.ru/" + str(item.find("div", {"class": (re.search("body-titleRow-\w+", str(item))).group()}).a["href"])



print(url_address)


