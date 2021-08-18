from helpers.setup import db, log

if __name__ == "__main__":
    log.info("Dropping previous template...")
    db.status.drop()
    log.info("Creating new template...")
    region: dict = {}
    for activity, locations in db.regions.find_one()["activities"].items():
        region[activity] = {}
        for location, parks in locations.items():
            region[activity][location] = {}
            for park_ID in parks:
                region[activity][location][park_ID] = {}
    log.info("Saving to database...")
    db.status.insert_one({"activities": region})
    log.info("Done")