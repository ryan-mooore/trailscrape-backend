from types import SimpleNamespace
from .shared import api
import logging

def main(park_ID, park: SimpleNamespace) -> dict:
    name = park["name"]
    logging.info(f"{name}:Making custom api call...")
    trails = api.get_trails(park)
    logging.info(f"{name}:Done")
    
    return {
        "parkIsOpen": True in [trail["isOpen"] for trail in trails],
        "trails": trails
    }