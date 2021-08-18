from typing import Any

from helpers.setup import log
from methods.shared import trailforks


def main(**kwargs: Any) -> bool:
    log.info(f"Making Trailforks api call...").add()
    park_status = trailforks.get_park_status(kwargs["info"]["regionID"])
    log.sub()
    return park_status
