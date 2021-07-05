from types import SimpleNamespace
from .shared import scrape
import logging

def main(park_ID, park: SimpleNamespace) -> dict:
    scrape_error = False
    park_status = None
    trails = None
    name = park["name"]
    try:
        logging.info(f"{name}:Getting scraping data...")
        scraper = scrape.get_scraper(park_ID)
        soup = scrape.get_soup(park)
        logging.info(f"{name}:Scraping (Trail status)...")
        trails = scraper.get_trails(soup)

        if park_status:
            logging.info(f"{name}:Scraping (Park status)...")
            park_status = scraper.get_park_status(soup)
        else:
            park_status = True in [trail["isOpen"] for trail in trails]
    
    except Exception as e:
        scrape_error = True
    logging.info(f"{name}:Done")
    
    return {
        "parkIsOpen": park_status,
        "trails": trails,
        "scrapeError": scrape_error
    }