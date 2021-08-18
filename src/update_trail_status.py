from helpers.setup import log
import re
from datetime import datetime
from importlib import import_module
from sys import argv

from helpers.setup import db, log
from helpers.chromedriver import driver
from helpers.types import MethodInterface
from other import weather

def import_method(modpath: list[str]) -> MethodInterface:
    return __import__(".".join(modpath).lower(), fromlist=['_trash'])

if __name__ == "__main__":
    log.info("Getting existing database entries...")
    regions = db.regions.find_one()
    status = db.status.find_one()
    log.info("Done")
    log.info("Updating trail status...").add()
    for activity, locations in regions["activities"].items():
        log.info(f"Updating {activity.title()} regions...").add()
        for region_ID, region in locations.items():
            log.info(f"Updating {region['name']} parks...").add()
            for park_ID, park in region["parks"].items():
                try:
                    if argv[1] and park_ID != argv[1]: continue
                except IndexError:
                    pass
                log.push()
                log.info(f"Updating {park['name']}...").add()
                new_status: dict = {}
                try:
                    for status_type, method in park["methods"].items():
                        log.info(f"Updating {status_type.title()} status...").add()
                        new_status[status_type] = import_method(
                            ["methods", "status", status_type, re.sub(r"(?<!^)(?=[A-Z])", "_", method["method"])]
                        ).main(park_ID=park_ID, info=method["info"], status=new_status)
                        log.sub().info(f"{status_type.title()} status: Done")
                    if not new_status["park"]:
                        log.info("Park is closed. Setting all trails to closed...")
                        for trail in new_status["trails"]:
                            trail["isOpen"] = False
                    log.info("Setting scrape information...")
                    new_status["scrapeError"] = False
                    new_status["scrapeTime"] = datetime.utcnow()
                    log.info("Updating weather...")
                    new_status["weather"] = {
                        "temp": weather.get_temp(**park["coords"]),
                        "conditions": weather.get_conditions(**park["coords"])
                    }
                    log.sub()
                except Exception as e:
                    log.pop().error(f"Error while scraping {park['name']}: {e}")
                    status["activities"][activity][region_ID]["parks"][park_ID]["scrapeError"] = True
                else:
                    status["activities"][activity][region_ID]["parks"][park_ID]["status"] = new_status
                    log.info(f"{park['name']}: Done")
            log.sub().info(f"{region['name']} parks: Done")
        log.sub().info(f"{activity.title()} regions: Done")
    log.sub().info("Saving to database...")
    db.status.update_one({"_id": status["_id"]}, {"$set": status})
    log.info("Done")