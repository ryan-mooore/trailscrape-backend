from typing import Any
from methods.shared import api
from helpers.types import Trails
from helpers.setup import log

def main(**kwargs: Any) -> Trails:
    log.info("Making custom api call...").add()
    trails = api.get_trails(kwargs["info"])
    log.sub()
    
    return trails