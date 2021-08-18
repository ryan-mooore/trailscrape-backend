from typing import Any


def main(**kwargs: Any) -> bool:
    return True in [trail["isOpen"] for trail in kwargs["status"]["trail"]]