from os import environ
import pymongo

client = pymongo.MongoClient(host=environ['MONGODB_URI'] if 'MONGODB_URI' in environ else 'localhost', port=27017)
db = client.trailscrape