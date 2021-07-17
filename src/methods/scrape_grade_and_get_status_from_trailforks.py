from types import SimpleNamespace
from .shared import scrape, trailforks
from difflib import get_close_matches
import logging

def main(park_ID, park: SimpleNamespace) -> dict:
    scrape_error = False
    trails = None
    name = park["name"]
    try:
        logging.info(f"{name}:Getting scraping data...")
        scraper = scrape.get_scraper(park_ID)
        soup = scrape.get_soup(park)
        logging.info(f"{name}:Scraping (Trail grades)...")
        trails = scraper.get_trails(soup)
        logging.info(f"{name}:Making Trailforks api call (Park status)...")
        park_status = trailforks.get_park_status(park)

        logging.info(f"{name}:Making Trailforks api call (Trail status)...")
        trailforks_trails = trailforks.get_trails(park)
        trailforks_trail_names = [trail["name"] for trail in trailforks_trails]
        logging.info(f"{name}:Matching trails to Trailforks trails...")
        for trail in trails:
            matches = get_close_matches(trail["name"], trailforks_trail_names)
            if matches:
                matched_trail = next((item for item in trailforks_trails if item["name"] == matches[0]), None)
                trail["isOpen"] = matched_trail["isOpen"]
                trail["trailforksName"] = matched_trail["trailforksName"]
                logging.info(f"Matched {matched_trail['name']} to {trail['name']}")

    except Exception as e:
        scrape_error = True
    logging.info(f"{name}:Done")

    return {
        "parkIsOpen": park_status,
        "trails": trails,
        "scrapeError": scrape_error
    }