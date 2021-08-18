import logging
from types import SimpleNamespace
from typing import Any

from helpers.types import Trails
from methods.shared import trailforks


def main(**kwargs: Any) -> Trails:
    logging.info(f"Making Trailforks api call (Park status)...")
    logging.info(f"Making Trailforks api call (Trail status)...")
    trails = trailforks.get_trails(kwargs["info"]["regionID"])
    logging.info(f"Done")
        
    return trails
