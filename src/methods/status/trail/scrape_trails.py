from typing import Any
from methods.shared import scrape
from helpers.types import Trails
import logging

def main(**kwargs: Any) -> Trails:
    trails = None

    scraper = scrape.get_scraper(kwargs["park_ID"])
    soup = scrape.get_soup(kwargs["info"])
    trails = scraper.get_trails(soup)

    return trails