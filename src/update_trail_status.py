from documents.documents import db
from datetime import datetime
import logging
from other import weather
from sys import argv
import importlib
import re

logging.basicConfig(level=20)

if __name__ == "__main__":
    regions = db.regions.find_one()
    status = db.status.find_one()
    for activity, locations in regions["activities"].items():
        for region_ID, region in locations.items():
            for park_ID, park in region["parks"].items():
                try:
                    if park_ID != argv[1]: continue
                finally:
                    new_status = {
                        "scrapeError": False
                    }
                    try:
                        new_status["status"] = importlib.import_module("methods." + re.sub(r"(?<!^)(?=[A-Z])", "_", park["method"]).lower()).main(park_ID, park)
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
