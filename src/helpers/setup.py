from os import environ

import pymongo  # type: ignore
from selenium import webdriver  # type: ignore
from webdriver_manager.chrome import ChromeDriverManager  # type: ignore

client: pymongo.MongoClient = pymongo.MongoClient(host=environ['MONGODB_URI'] if 'MONGODB_URI' in environ else 'localhost', port=27017)
db = client.trailscrape

options = webdriver.ChromeOptions()
options.add_argument("headless")
driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
