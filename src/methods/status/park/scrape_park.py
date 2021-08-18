from typing import Any
from methods.shared import scrape
import logging

def main(**kwargs: Any) -> bool:
    park_status = None
    
    logging.info("Getting scraping data...")
    scraper = scrape.get_scraper(kwargs["park_ID"])
    soup = scrape.get_soup(kwargs["info"])
    
    logging.info("Scraping (Park status)...")
    park_status = scraper.get_park_status(soup)

    return park_status
