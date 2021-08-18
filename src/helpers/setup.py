import logging
from os import environ

import pymongo  # type: ignore
from python_log_indenter import IndentedLoggerAdapter # type: ignore

logging.basicConfig(level=logging.INFO, format='%(message)s')
log = IndentedLoggerAdapter(logging.getLogger())

log.info("Connecting to database...")
client: pymongo.MongoClient = pymongo.MongoClient(host=environ['MONGODB_URI'] if 'MONGODB_URI' in environ else 'localhost', port=27017)
db = client.trailscrape
log.info("Done")

