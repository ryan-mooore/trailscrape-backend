import logging
import re
from datetime import datetime
from importlib import import_module
from sys import argv

from helpers.setup import db
from helpers.types import MethodInterface
from other import weather

logging.basicConfig(level=20)

def import_method(modpath: list[str]) -> MethodInterface:
    return __import__(".".join(modpath).lower(), fromlist=['_trash'])

if __name__ == "__main__":
    regions = db.regions.find_one()
    status = db.status.find_one()
    for activity, locations in regions["activities"].items():
        for region_ID, region in locations.items():
            for park_ID, park in region["parks"].items():
                try:
                    if argv[1] and park_ID != argv[1]: continue
                except IndexError:
                    pass
                new_status: dict = {}
                try:
                    for status_type, method in park["methods"].items():
                        new_status[status_type] = import_method(
                            ["methods", "status", status_type, re.sub(r"(?<!^)(?=[A-Z])", "_", method["method"])]
                        ).main(park_ID=park_ID, info=method["info"], status=new_status)
                    new_status["scrapeError"] = False
                    new_status["scrapeTime"] = datetime.utcnow()
                    new_status["weather"] = {
                        "temp": weather.get_temp(**park["coords"]),
                        "conditions": weather.get_conditions(**park["coords"])
                    }
                except Exception as e:
                    print(f"Error while scraping {park['name']}: {e}")
                    status["activities"][activity][region_ID]["parks"][park_ID]["scrapeError"] = True
                else:
                    status["activities"][activity][region_ID]["parks"][park_ID] = new_status
    db.status.update_one({"_id": status["_id"]}, {"$set": status})