from types import SimpleNamespace
from typing import Any

from helpers.types import Trails
from helpers.setup import log
from methods.shared import trailforks


def main(**kwargs: Any) -> Trails:
    log.info(f"Making Trailforks api call...").add()
    trails = trailforks.get_trails(kwargs["info"]["regionID"])
    log.sub()
        
    return trails
