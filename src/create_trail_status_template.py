from collections import defaultdict
from documents.documents import db

if __name__ == "__main__":
    db.region_status.drop()
    region_status = {}
    for activity, locations in db.region.find_one()["activities"].items():
        region_status[activity] = {}
        for location, parks in locations.items():
            region_status[activity][location] = {}
            for park_ID in parks:
                region_status[activity][location][park_ID] = {}
    db.region_status.insert_one(region_status)