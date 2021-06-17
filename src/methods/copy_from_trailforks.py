from types import SimpleNamespace
from .shared import scrape, trailforks
import logging
def main(region: SimpleNamespace) -> dict:
    logging.info(f"{region.name}:Making Trailforks api call (Park status)...")
    park_is_open = trailforks.get_park_status(region)
    logging.info(f"{region.name}:Making Trailforks api call (Trail status)...")
    trails = trailforks.get_trails(region)
    logging.info(f"{region.name}:Done")
    return {
        "parkIsOpen": park_is_open,
        "trails": trails,
    }