from documents.documents import db
from os import path
from json import load
import logging

logging.basicConfig(level=20)

if __name__ == "__main__":
    logging.info("Dropping collection...")
    db.regions.drop()
    logging.info("Updating regions...")
    with open(path.join(path.dirname(__file__), '../regions.json'), 'r') as regions:
        db.regions.insert_one(load(regions))
    logging.info("Done")