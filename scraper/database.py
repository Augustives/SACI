import os
from typing import Dict, List

from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.operations import UpdateOne

from scraper.settings import DATABASE_NAME

FIELDS_TO_UPDATE = [
    "name",
    "time_complexity",
    "trustable_time_complexity",
    "space_complexity",
    "trustable_space_complexity",
]


class ScraperDatabase:
    def __init__(self):
        self.client: MongoClient = MongoClient(
            os.environ.get("MONGO_CONNECTION_STRING"), serverSelectionTimeoutMS=1
        )
        self.database = self.client[DATABASE_NAME]

    def _get_collection(self, collection_name: str) -> Collection:
        return self.database[collection_name]

    def update_database(self, collection_name: str, data: List[Dict[str, any]]):
        collection = self._get_collection(collection_name)
        operations = [
            UpdateOne(
                filter={"url": item["url"], "codes": item["codes"]},
                update={"$set": {field: item[field] for field in FIELDS_TO_UPDATE}},
                upsert=True,
            )
            for item in data
        ]
        collection.bulk_write(operations)
