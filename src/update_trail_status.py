from types import SimpleNamespace
from documents.documents import db
from methods import scrape_park_and_get_trails_from_trailforks, api, copy_from_trailforks, scrape_trails, scrape_status_and_get_grade_from_trailforks
from datetime import datetime
import logging

logging.basicConfig(level=20)

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
                    for k, v in {
                        "scrapeTrails": scrape_trails,
                        "scrapeParkAndGetTrailsFromTrailforks": scrape_park_and_get_trails_from_trailforks,
                        "scrapeStatusAndGetGradeFromTrailforks": scrape_status_and_get_grade_from_trailforks,
                        "copyFromTrailforks": copy_from_trailforks,
                        "api": api
                    }[park["method"]].main(park_ID, park).items():
                        new_status[k] = v
                        new_status["scrapeTime"] = datetime.utcnow()
                except Exception as e:
                    print(f"Error while scraping {park['name']}: {e}")
                    status["activities"][activity][region_ID][park_ID].scrapeError = True
                else:
                    status["activities"][activity][region_ID][park_ID] = new_status
    db.status.update_one({"_id": status["_id"]}, {"$set": status})
