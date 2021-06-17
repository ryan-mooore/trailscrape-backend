from documents.documents import Region
from os import path
from json import load
import logging

logging.basicConfig(level=20)

if __name__ == "__main__":
    logging.info("Dropping collection...")
    Region.drop_collection()
    logging.info("Updating regions...")
    with open(path.join(path.dirname(__file__), '../regions.json'), 'r') as regions:
        for region in load(regions):
            entry = Region(**region)
            entry.save()
    logging.info("Done")