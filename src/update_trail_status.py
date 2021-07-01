from types import SimpleNamespace
from documents.documents import db
from methods import scrape_park_and_get_trails_from_trailforks, api, copy_from_trailforks, scrape_trails, scrape_status_and_get_grade_from_trailforks
from datetime import datetime
import logging

logging.basicConfig(level=20)

if __name__ == "__main__":
    region_status_json = {}
    region = db.region.find_one()
    region_status = db.region_status.find_one()
    for activity, locations in region["activities"].items():
        for location, parks in locations.items():
            for park_ID, park in parks.items():
                status = {
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
                        status[k] = v
                except Exception as e:
                    print(f"Error while scraping {park['name']}: {e}")
                    region_status["activities"][activity][location][park_ID].scrapeError = True
                else:
                    region_status["activities"][activity][location][park_ID] = status