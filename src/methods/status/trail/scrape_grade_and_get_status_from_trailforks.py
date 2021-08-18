import logging
from difflib import get_close_matches
from typing import Any

from helpers.types import Trails
from methods.shared import scrape, trailforks


def main(**kwargs: Any) -> Trails:
    trails = None
    
    logging.info("Getting scraping data...")
    scraper = scrape.get_scraper(kwargs["park_ID"])
    soup = scrape.get_soup(kwargs["info"])
    logging.info("Scraping (Trail grades)...")
    trails = scraper.get_trails(soup)

    logging.info("Making Trailforks api call (Trail status)...")
    trailforks_trails = trailforks.get_trails(kwargs["info"]["regionID"])
    trailforks_trail_names = [trail["name"] for trail in trailforks_trails]
    logging.info(f"Matching trails to Trailforks trails...")
    for trail in trails:
        matches = get_close_matches(trail["name"], trailforks_trail_names)
        if matches:
            matched_trail = next((item for item in trailforks_trails if item["name"] == matches[0]), None)
            if matched_trail:
                trail["isOpen"] = matched_trail["isOpen"]
                trail["trailforksName"] = matched_trail["trailforksName"]
                logging.info(f"Matched {matched_trail['name']} to {trail['name']}")

    return trails
