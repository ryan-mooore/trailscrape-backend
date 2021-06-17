from types import SimpleNamespace
from .shared import api
import logging

def main(region: SimpleNamespace) -> dict:
    logging.info(f"{region.name}:Making custom api call...")
    trails = api.get_trails(region)
    logging.info(f"{region.name}:Done")
    
    return {
        "parkIsOpen": True in [trail["isOpen"] for trail in trails],
        "trails": trails
    }