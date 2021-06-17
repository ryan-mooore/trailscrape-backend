from types import SimpleNamespace
from .shared import scrape, trailforks
import logging

def main(region: SimpleNamespace) -> dict:
    scrape_error = False
    park_status = None
    try:
        logging.info(f"{region.name}:Getting scraping data...")
        scraper = scrape.get_scraper(region)
        soup = scrape.get_soup(region)
        logging.info(f"{region.name}:Scraping (Park status)...")
        park_status = scraper.get_park_status(soup)
        logging.info(f"{region.name}:Making Trailforks api call (Trail status)...")
        trails = trailforks.get_trails(region)
    except Exception as e:
        scrape_error = True
    logging.info(f"{region.name}:Done")
    
    return {
        "parkIsOpen": park_status,
        "trails": trails,
        "scrapeError": scrape_error
    }