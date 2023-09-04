from asyncio import gather

from scraper.database import ScraperDatabase
from scraper.settings import USE_MONGO_DATABASE
from scraper.utils import write_results_to_json
from scraper.websites import websites


async def run_scrapers():
    scrapers_results = await gather(*[scraper() for scraper in websites.values()])
    for name, data in zip(websites.keys(), scrapers_results):
        if USE_MONGO_DATABASE:
            database = ScraperDatabase()
            database.update_database(name, [result.dict() for result in data])
        else:
            write_results_to_json(
                name,
                sorted([result.dict() for result in data], key=lambda alg: alg["url"]),
            )
