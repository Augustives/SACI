from asyncio import get_event_loop

from scraper.runner import run_scrapers

if __name__ == "__main__":
    loop = get_event_loop()
    loop.run_until_complete(run_scrapers())
