import importlib
from types import ModuleType, SimpleNamespace
from helpers.chromedriver import driver

from requests import get

from helpers.types import ScraperInterface

from bs4 import BeautifulSoup as BS # type: ignore
from selenium import webdriver # type: ignore

def get_soup(info: dict) -> BS:

    if info["withChromedriver"]:
        driver.get(info["url"])
        return BS(driver.page_source, "html.parser")

    else:
        content = get(info["url"])
        return BS(content.text, "html.parser")

def get_scraper(park_ID: str) -> ScraperInterface:
    return __import__("scrapers." + park_ID.replace("-", "_"), fromlist=['_trash'])