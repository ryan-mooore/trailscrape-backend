from types import SimpleNamespace, ModuleType
import requests
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
from bs4 import BeautifulSoup as BS
import importlib

def get_driver() -> webdriver.Chrome:
    options = webdriver.ChromeOptions()
    options.add_argument("headless")
    return webdriver.Chrome(ChromeDriverManager().install(), options=options)


def get_soup(region: SimpleNamespace):

    if region.methodInfo["withChromedriver"]:
        driver = get_driver()
        driver.get(region.methodInfo["url"])
        sleep(2)
        return BS(driver.page_source, "html.parser")

    else:
        content = requests.get(region.methodInfo["url"])
        return BS(content.text, "html.parser")

def get_scraper(region: SimpleNamespace) -> ModuleType:
    return importlib.import_module(
    "scrapers." + region.ID)