from asyncio import gather

from scraper.database import Database
from scraper.settings import USE_MONGO_DATABASE
from scraper.utils import write_results_to_json
from scraper.websites import scrapers


async def run_scrapers():
    scrapers_results = await gather(*[scraper() for scraper in scrapers.values()])
    for name, data in zip(scrapers.keys(), scrapers_results):
        if USE_MONGO_DATABASE:
            database = Database()
            database.update_database(name, data)
        else:
            write_results_to_json(name, data)
