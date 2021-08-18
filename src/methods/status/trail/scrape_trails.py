from typing import Any
from methods.shared import scrape
from helpers.types import Trails
from helpers.setup import log

def main(**kwargs: Any) -> Trails:
    trails = None

    log.info("Requesting website data...").add()
    scraper = scrape.get_scraper(kwargs["park_ID"])
    soup = scrape.get_soup(kwargs["info"])
    log.sub().info("Scraping trails...").add()
    trails = scraper.get_trails(soup)
    log.sub()

    return trails