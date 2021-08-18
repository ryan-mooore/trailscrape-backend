from typing import Any
from methods.shared import scrape, trailforks
from helpers.types import Trails
from difflib import get_close_matches
from helpers.setup import log

def main(**kwargs: Any) -> Trails:
    trails = None
    log.info("Requesting website data...")
    scraper = scrape.get_scraper(kwargs["park_ID"])
    soup = scrape.get_soup(kwargs["info"])
    log.info(f"Scraping trails...")
    trails = scraper.get_trails(soup)

    log.info(f"Making Trailforks api call...")
    trailforks_trails = trailforks.get_trails(kwargs["info"]["regionID"])
    trailforks_trail_names = [trail["name"] for trail in trailforks_trails]
    log.info(f"Matching trails to Trailforks trails...")
    for trail in trails:
        matches = get_close_matches(trail["name"], trailforks_trail_names)
        if matches:
            matched_trail = next((item for item in trailforks_trails if item["name"] == matches[0]), None)
            if matched_trail:
                trail["grade"] = matched_trail["grade"]
                log.debug(f"Matched {matched_trail['name']} to {trail['name']}")

    return trails