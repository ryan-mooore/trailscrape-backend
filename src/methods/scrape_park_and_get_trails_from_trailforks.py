from types import SimpleNamespace
from .shared import scrape, trailforks
import logging

def main(park_ID, park: SimpleNamespace) -> dict:
    scrape_error = False
    park_status = None
    name = park["name"]
    try:
        logging.info(f"{name}:Getting scraping data...")
        scraper = scrape.get_scraper(park_ID)
        soup = scrape.get_soup(park)
        logging.info(f"{name}:Scraping (Park status)...")
        park_status = scraper.get_park_status(soup)
        logging.info(f"{name}:Making Trailforks api call (Trail status)...")
        trails = trailforks.get_trails(park)
    except Exception as e:
        scrape_error = True
    logging.info(f"{name}:Done")
    
    return {
        "parkIsOpen": park_status,
        "trails": trails,
        "scrapeError": scrape_error
    }