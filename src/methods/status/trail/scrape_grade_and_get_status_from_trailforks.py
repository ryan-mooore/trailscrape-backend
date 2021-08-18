from helpers.setup import log
from difflib import get_close_matches
from typing import Any

from helpers.types import Trails
from methods.shared import scrape, trailforks


def main(**kwargs: Any) -> Trails:
    trails = None
    
    log.info("Requesting website data...").add()
    scraper = scrape.get_scraper(kwargs["park_ID"])
    soup = scrape.get_soup(kwargs["info"])
    log.sub().info("Scraping trails...").add()
    trails = scraper.get_trails(soup)

    log.sub().info("Making Trailforks api call...").add()
    trailforks_trails = trailforks.get_trails(kwargs["info"]["regionID"])
    trailforks_trail_names = [trail["name"] for trail in trailforks_trails]
    log.sub().info(f"Matching trails to Trailforks trails...").add()
    for trail in trails:
        matches = get_close_matches(trail["name"], trailforks_trail_names)
        if matches:
            matched_trail = next((item for item in trailforks_trails if item["name"] == matches[0]), None)
            if matched_trail:
                trail["isOpen"] = matched_trail["isOpen"]
                trail["trailforksName"] = matched_trail["trailforksName"]
                log.debug(f"Matched {matched_trail['name']} to {trail['name']}")
    log.sub()

    return trails
