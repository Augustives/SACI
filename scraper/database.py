import os

from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database
from pymongo.operations import UpdateOne

from scraper.settings import DATABASE_NAME


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
                UpdateOne(
                    update={
                        "$set": {
                            "name": item["name"],
                            "time_complexity": item["time_complexity"],
                            "trustable_time_complexity": item[
                                "trustable_time_complexity"
                            ],
                            "space_complexity": item["space_complexity"],
                            "trustable_space_complexity": item[
                                "trustable_space_complexity"
                            ],
                        }
                    },
                    filter={"url": item["url"], "codes": item["codes"]},
                    upsert=True,
                )
                for item in data
            ]
        )
