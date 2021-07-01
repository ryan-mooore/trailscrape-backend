from collections import defaultdict
from documents.documents import db

if __name__ == "__main__":
    db.status.drop()
    region = {}
    for activity, locations in db.regions.find_one()["activities"].items():
        region[activity] = {}
        for location, parks in locations.items():
            region[activity][location] = {}
            for park_ID in parks:
                region[activity][location][park_ID] = {}
    db.status.insert_one({"activities": region})