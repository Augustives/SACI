from asyncio import gather

from scraper.websites import scrapers


async def run_scrapers():
    await gather(
        *[
            scraper()
            for scraper in scrapers.values()
        ]
    )
