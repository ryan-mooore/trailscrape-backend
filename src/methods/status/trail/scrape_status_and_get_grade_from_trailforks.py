from typing import Any
from methods.shared import scrape, trailforks
from helpers.types import Trails
from difflib import get_close_matches
import logging

def main(**kwargs: Any) -> Trails:
    trails = None
    logging.info(f"Getting scraping data...")
    scraper = scrape.get_scraper(kwargs["park_ID"])
    soup = scrape.get_soup(kwargs["info"])
    logging.info(f"Scraping (Trail status)...")
    trails = scraper.get_trails(soup)

    logging.info(f"Making Trailforks api call (Trail grades)...")
    trailforks_trails = trailforks.get_trails(kwargs["info"]["regionID"])
    trailforks_trail_names = [trail["name"] for trail in trailforks_trails]
    logging.info(f"Matching trails to Trailforks trails...")
    for trail in trails:
        matches = get_close_matches(trail["name"], trailforks_trail_names)
        if matches:
            matched_trail = next((item for item in trailforks_trails if item["name"] == matches[0]), None)
            if matched_trail:
                trail["grade"] = matched_trail["grade"]
                logging.info(f"Matched {matched_trail['name']} to {trail['name']}")

    logging.info(f"Done")
    return trails