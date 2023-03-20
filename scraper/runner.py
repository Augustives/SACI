from asyncio import gather

from scraper.database import Database
from scraper.websites import scrapers


async def run_scrapers():
    database = Database()
    scrapers_results = await gather(*[scraper() for scraper in scrapers.values()])
    for name, data in zip(scrapers.keys(), scrapers_results):
        database.update_database(name, data)
