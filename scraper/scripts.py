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


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--script")
    parser.add_argument("--url", help="URL to be extracted.")
    parser.add_argument("--scraper", help="Scraper to be used.")
    args = parser.parse_args()

    actions = {
        "scrape_url": lambda: extract_single_url(args.url, args.scraper),
        "results_analysis": lambda: make_results_analysis(args.scraper),
        "manual_results_boilerplate": lambda: make_manual_results_boilerplate(
            args.scraper
        ),
    }

    action = actions.get(args.script)
    if action:
        action()
    else:
        print(f"Unknown script: {args.script}")


if __name__ == "__main__":
    main()
