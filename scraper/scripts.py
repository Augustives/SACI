import argparse
import pprint

from asyncio import get_event_loop
from importlib import import_module


from scraper.observability.metrics import (
    make_results_analysis,
    make_manual_results_boilerplate,
)


def extract_single_url(url: str, scraper: str):
    module = import_module(f"scraper.websites.{scraper}")
    spider = getattr(module, "spider")

    loop = get_event_loop()
    result = loop.run_until_complete(spider.run(url))
    pprint.PrettyPrinter(indent=4).pprint(result)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--script")
    parser.add_argument("--url", help="URL to be extracted.")
    parser.add_argument("--scraper", help="URL to be extracted.")
    args = parser.parse_args()

    match args.script:
        case "scrape_url":
            extract_single_url(args.url, args.scraper)
        case "results_analysis":
            make_results_analysis(args.scraper)
        case "manual_results_boilerplate":
            make_manual_results_boilerplate(args.scraper)
