from typing import Any
from methods.shared import scrape
from helpers.setup import log

def main(**kwargs: Any) -> bool:
    park_status = None
    
    log.info("Requesting website data...").add()
    scraper = scrape.get_scraper(kwargs["park_ID"])
    soup = scrape.get_soup(kwargs["info"])
    
    log.sub().info("Scraping park status...").add()
    park_status = scraper.get_park_status(soup)
    log.sub()

    return park_status
