from typing import Any
from methods.shared import api
from helpers.types import Trails
import logging

def main(**kwargs: Any) -> Trails:
    logging.info("Making custom api call...")
    trails = api.get_trails(kwargs["info"])
    
    return trails