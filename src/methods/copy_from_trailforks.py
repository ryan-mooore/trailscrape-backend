from types import SimpleNamespace
from .shared import scrape, trailforks
import logging
def main(park_ID, park: SimpleNamespace) -> dict:
    name = park["name"]
    logging.info(f"{name}:Making Trailforks api call (Park status)...")
    park_status = trailforks.get_park_status(park)
    logging.info(f"{name}:Making Trailforks api call (Trail status)...")
    trails = trailforks.get_trails(park)
    logging.info(f"{name}:Done")
        
    if not park_status:
        for trail in trails:
            trail["isOpen"] = False
        
    return {
        "parkIsOpen": park_status,
        "trails": trails,
    }