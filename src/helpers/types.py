from typing import Any, Union

from bs4 import BeautifulSoup # type: ignore

Trails = list[dict[str, Any]]

class MethodInterface():
    @staticmethod
    def main(park_ID: str, park: dict, status: dict) -> Any: ...

class ScraperInterface():
    @staticmethod
    def get_trails(soup: BeautifulSoup) -> Trails: ...
    @staticmethod
    def get_park_status(soup: BeautifulSoup) -> bool: ...
    @staticmethod
    def get_lift_status(soup: BeautifulSoup) -> bool: ...
