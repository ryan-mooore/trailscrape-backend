from types import SimpleNamespace
from .shared import scrape
import logging

def main(region: SimpleNamespace) -> dict:
    scrape_error = False
    park_status = None
    trails = None
    try:
        logging.info(f"{region.name}:Getting scraping data...")
        scraper = scrape.get_scraper(region)
        soup = scrape.get_soup(region)
        logging.info(f"{region.name}:Scraping (Trail status)...")
        trails = scraper.get_trails(soup)

        if park_status:
            logging.info(f"{region.name}:Scraping (Park status)...")
            park_status = scraper.get_park_status(soup)
        else:
            park_status = True in [trail["isOpen"] for trail in trails]
    
    except Exception as e:
        scrape_error = True
    logging.info(f"{region.name}:Done")
    
    return {
        "parkIsOpen": park_status,
        "trails": trails,
        "scrapeError": scrape_error
    }