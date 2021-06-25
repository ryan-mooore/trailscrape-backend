from typing import Union
from os import environ
from mongoengine import connect
from mongoengine.document import Document
from mongoengine.fields import (BooleanField, DictField, DynamicField, ListField,
                                StringField, DateTimeField, IntField)

client = connect(db="trailscrape", host=environ['MONGODB_URI'] if 'MONGODB_URI' in environ else 'localhost', port=27017)

class Region(Document):
    ID: str = StringField(required=True, unique=True, max_length=3)
    name: str = StringField(required=True)
    method: str = StringField(required=True)
    methodInfo: dict = DynamicField()
    hasUplifts: bool = BooleanField(required=True)


class RegionStatus(Document):
    ID: str = StringField(required=True, unique=True, max_length=3)
    scrapeError: bool = BooleanField(required=True)
    trails: list[dict] = ListField()
    parkIsOpen: bool = BooleanField()
    liftIsOpen: bool = BooleanField()
    scrapeTime = DateTimeField()

class TrailforksRegion(Document):
    str_ID: str = StringField(required=True)
    num_ID: int = IntField(required=True)
    trails: dict = DictField()
