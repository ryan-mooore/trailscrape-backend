from types import SimpleNamespace
from .shared import scrape, trailforks
from difflib import get_close_matches
import logging

def main(region: SimpleNamespace) -> dict:
    scrape_error = False
    trails = None
    try:
        logging.info(f"{region.name}:Getting scraping data...")
        scraper = scrape.get_scraper(region)
        soup = scrape.get_soup(region)
        logging.info(f"{region.name}:Scraping (Trail status)...")
        trails = scraper.get_trails(soup)
        logging.info(f"{region.name}:Making Trailforks api call (Park status)...")
        park_status = trailforks.get_park_status(region)

        logging.info(f"{region.name}:Making Trailforks api call (Trail status)...")
        trailforks_trails = trailforks.get_trails(region)
        trailforks_trail_names = [trail["name"] for trail in trailforks_trails]
        logging.info(f"{region.name}:Matching trails to Trailforks trails...")
        for trail in trails:
            matches = get_close_matches(trail["name"], trailforks_trail_names)
            if matches:
                matched_trail = next((item for item in trailforks_trails if item["name"] == matches[0]), None)
                trail["grade"] = matched_trail["grade"]
                logging.info(f"Matched {matched_trail['name']} to {trail['name']}")

    except Exception as e:
        scrape_error = True
    logging.info(f"{region.name}:Done")

    return {
        "parkIsOpen": park_status,
        "trails": trails,
        "scrapeError": scrape_error
    }