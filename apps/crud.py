from dateutil.parser import parse
import re

import requests
from bs4 import BeautifulSoup as BS
import pandas as pd

from db import database


HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.1 Safari/605.1.15"
}


def get_soup(url: str) -> BS:
    """
    Execute a get request on the given URL and create a soup object

    :param url: str
    A get request is made at this URL

    :return: BeautifulSoup object
    """
    html = requests.get(url, headers=HEADERS).text
    soup = BS(html, "lxml")
    return soup

def get_price_eur(price_rub: str, eur_value: str) -> float:
    """
    Get price in euro

    :param price_rub: str
    Price in rubles

    :param eur_value: str
    Cost 1 euro

    :return: str
    """
    return round((float(price_rub) / float(eur_value)), 2)

def get_eur_value() -> [str, str]:
    """
    Obtaining the current euro exchange rate from the website of the Central Bank of Russia

    :return: list[str, str]
    Cost 1 euro, course date
    """
    data = requests.get('https://www.cbr-xml-daily.ru/daily_json.js').json()
    eur_value = data["Valute"]["EUR"]["Value"]
    date_eur_value = data["Date"]
    return eur_value, date_eur_value

def get_dataframe(url:str) -> pd.DataFrame:
    """
    Performing page parsing at the given URL and creating a Dataframe.

    :param url: str
    A get request is made at this URL

    :return: Dataframe
    """
    soup = get_soup(url)
    dataframe = pd.DataFrame()
    eur_value, date_eur_value = get_eur_value()
    date_eur_value = (parse(date_eur_value)).date()
    items = (soup.find(
        "div", {"id": "app"})).find("div", {"class": (re.search("styles-list-\w+", str(soup))).group()}).findAll(
        "div",{"class": (re.search("styles-item-\w+",str(soup))).group()})
    for item in items:
        title = item.find("div", {"class": (re.search("body-titleRow-\w+", str(item))).group()}).a["title"]
        price_value_rub = item.find("div", {"class": (re.search("body-priceRow-\w+", str(item))).group()}).find("meta", {"itemprop": "price"})["content"]
        price_value_eur = get_price_eur(price_value_rub, eur_value)
        price_note = (item.find("span", {
            "class": (re.search("price-text-\w+\s\w+-\w+-\w+\s\w+-\w+-\w+-\w+", str(item))).group()})).contents
        if len(price_note) > 4:
            price_note = price_note[-1]
        else:
            price_note = None
        placement_date = item.find("span", {
            "class": (re.search("text-text-LurtD\s\w+-\w+-\w+-\w+\s\w+-\w+-\w+-\w+", str(item))).group()}).string
        photo_url = (item.find("div", {"class": (re.search("photo-slider-item-\w+", str(item))).group()})).img["src"]
        url_address = "https://www.avito.ru/" + str(
            item.find("div", {"class": (re.search("body-titleRow-\w+", str(item))).group()}).a["href"])
        id, _ = (url_address[::-1]).split('_', 1)
        dataframe = pd.concat([dataframe,
                               pd.DataFrame({
                                   'id': [id],
                                   'description': [title],
                                   'price_in_rub': [price_value_rub],
                                   'price_in_eur': [f"{price_value_eur} на {str(date_eur_value)}"],
                                   'price_note': [price_note],
                                   'placement_date': [placement_date],
                                   'photo_url': [photo_url],
                                   'url_address': [url_address]

                               })], ignore_index=True)
    return dataframe

def create_announcements(dataframe: pd.DataFrame) -> None:
    """
    Write dataframe to database.

    :param dataframe: Dataframe

    :return: None
    """
    announcements = dataframe.to_sql('announcements', con=database.engine, if_exists='append', index=False)
    return announcements
