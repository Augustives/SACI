import os

from pymongo import MongoClient
from pymongo.database import Database
from pymongo.collection import Collection
from pymongo.operations import ReplaceOne

from scraper.settings import DATABASE_NAME, COLLECTION_NAME


class Database:
    def __init__(self):
        self.client: MongoClient = MongoClient(
            os.environ.get("MONGO_CONNECTION_STRING"), serverSelectionTimeoutMS=1
        )
        self.database: Database = self.client[DATABASE_NAME]

    def _get_collection(self, collection_name: str) -> Collection:
        return self.database[collection_name]

    def update_database(self, collection_name: str, data: list):
        collection = self._get_collection(collection_name)

        collection.bulk_write(
            [
                ReplaceOne(
                    replacement=item,
                    filter={"url": item["url"], "algorithm": item["algorithm"]},
                    upsert=True,
                )
                for item in data
            ]
        )
