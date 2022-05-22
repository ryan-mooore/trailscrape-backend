from os import environ
from typing import Any

import requests
from helpers.setup import log


def main(**kwargs: Any) -> bool:
    log.info(f"Making Gmaps api call...").add()
    lift_status = requests.get(
        f"https://maps.googleapis.com/maps/api/place/details/json?key={environ['GMAPS_API_KEY']}&placeid={kwargs['info']['placeID']}"
    ).json()["result"]["opening_hours"]["open_now"]
    log.sub()
    return lift_status