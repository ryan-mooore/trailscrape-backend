from types import SimpleNamespace
from documents.documents import Region, RegionStatus
from methods import scrape_park_and_get_trails_from_trailforks, api, copy_from_trailforks, scrape_trails, scrape_status_and_get_grade_from_trailforks
from datetime import datetime
import logging

logging.basicConfig(level=20)

if __name__ == "__main__":
    for region in Region.objects:
        try:
            region_status = RegionStatus.objects(ID=region.ID)[0]
            region_status.scrapeError = False
        except IndexError:
            region_status = RegionStatus(
                ID=region.ID, scrapeError=False)
        try:
            for (k, v) in {
                "scrapeTrails": scrape_trails,
                "scrapeParkAndGetTrailsFromTrailforks": scrape_park_and_get_trails_from_trailforks,
                "scrapeStatusAndGetGradeFromTrailforks": scrape_status_and_get_grade_from_trailforks,
                "copyFromTrailforks": copy_from_trailforks,
                "api": api
            }[region.method].main(region).items():
                setattr(region_status, k, v)
        except Exception as e:
            print(f"Error while scraping {region.name}: {e}")
            region_status.scrapeError = True
        region_status.save()