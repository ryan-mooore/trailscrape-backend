from typing import Any
from helpers.setup import log

def main(**kwargs: Any) -> bool:
    log.info("Inferring lift status from trail status...")
    return True in [trail["isOpen"] for trail in kwargs["status"]["trails"]] and kwargs["status"]["park"]