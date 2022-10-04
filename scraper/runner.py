from asyncio import gather

from scraper.logger import log
from scraper.websites import scrapers


async def run_scrapers():
    log.info('Running scraping operations')
    await gather(
        *[
            scraper
            for scraper in scrapers.values()
        ]
    )
