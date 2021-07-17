from types import SimpleNamespace
from documents.documents import db
from methods import scrape_park_and_get_trails_from_trailforks, api, copy_from_trailforks, scrape_trails, scrape_status_and_get_grade_from_trailforks
from datetime import datetime
import logging
from other import weather

logging.basicConfig(level=20)

method_map = {
    "scrapeTrails": scrape_trails,
    "scrapeParkAndGetTrailsFromTrailforks": scrape_park_and_get_trails_from_trailforks,
    "scrapeStatusAndGetGradeFromTrailforks": scrape_status_and_get_grade_from_trailforks,
    "copyFromTrailforks": copy_from_trailforks,
    "api": api
}

if __name__ == "__main__":
    regions = db.regions.find_one()
    status = db.status.find_one()
    for activity, locations in regions["activities"].items():
        for region_ID, region in locations.items():
            for park_ID, park in region["parks"].items():
                new_status = {
                    "scrapeError": False
                }
                try:
                    new_status["status"] = method_map[park["method"]].main(park_ID, park)
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
