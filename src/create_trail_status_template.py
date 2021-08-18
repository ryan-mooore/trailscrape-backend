from helpers.setup import db, log

if __name__ == "__main__":
    log.info("Dropping previous template...")
    db.status.drop()
    log.info("Creating new template...")
    region: dict = {}
    for activity, locations in db.regions.find_one()["activities"].items():
        region[activity] = {}
        for location_ID, location in locations.items():
            region[activity][location_ID] = {}
            region[activity][location_ID]["name"] = location["name"]
            region[activity][location_ID]["parks"] = {park_id: {} for park_id, park in location["parks"].items()}

    log.info("Saving to database...")
    db.status.insert_one({"activities": region})
    log.info("Done")