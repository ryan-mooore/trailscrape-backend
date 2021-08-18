from typing import Any
from methods.shared import trailforks

def main(**kwargs: Any) -> bool:
    return trailforks.get_park_status(kwargs["info"]["regionID"])