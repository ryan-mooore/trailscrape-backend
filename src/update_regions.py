from helpers.setup import db
from os import path
from json import load
from helpers.setup import log

if __name__ == "__main__":
    log.info("Dropping collection...")
    db.regions.drop()
    log.info("Updating regions...")
    with open(path.join(path.dirname(__file__), '../regions.json'), 'r') as regions:
        db.regions.insert_one(load(regions))
    log.info("Done")