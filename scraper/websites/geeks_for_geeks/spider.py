from asyncio import gather

from scraper.observability.log import scraper_log as log
from scraper.observability.metric import calculate_completition_rate
from scraper.schema import SCRAPER_OUTPUT, Schema
from scraper.session.http_session import HttpSession
from scraper.session.response import Response
from scraper.session.utils import Methods
from scraper.websites.geeks_for_geeks.extract import extract
from scraper.websites.geeks_for_geeks.settings import ALGORITHMS_LOCATION_URLS, HEADERS


# ------- PARSERS -------
def parse_algorithm_schema(algorithm_data: dict):
    if algorithm_data:
        for algorithm in algorithm_data:
            algorithm_schema = Schema(algorithm, SCRAPER_OUTPUT)
            algorithm_schema.validate()
    return algorithm_data


# ------- FILTERS -------
def filter_algorithms_urls(alorithms_urls: list):
    return list(filter(lambda href: ("geeksquiz" not in href), alorithms_urls))


# ------- EXTRACTORS -------
def extract_algorithm_data(response: Response):
    if response:
        data = extract(response)
        if data:
            return data
    return []


def extract_algorithms_urls(response: Response):
    page_content = response.soup.find("div", {"class": "page_content"})
    return list(
        filter(
            None,
            [
                a.attrs.get("href")
                for ol in page_content.find_all("ol")[1:]
                for a in ol.find_all("a")
            ],
        )
    )


# ------- FOLLOWS -------
async def follow_algorithms(session: HttpSession, algorithms_urls: list):
    algorithms = await gather(
        *[
            session.request(
                method=Methods.GET.value,
                url=url,
                callbacks=[extract_algorithm_data, parse_algorithm_schema],
            )
            for url in algorithms_urls
        ]
    )
    return sum(algorithms, [])


async def follow_algorithms_urls(session: HttpSession):
    algorithm_location_urls = await gather(
        *[
            session.request(
                method=Methods.GET.value,
                url=url,
                callbacks=[extract_algorithms_urls, filter_algorithms_urls],
            )
            for url in ALGORITHMS_LOCATION_URLS
        ]
    )
    return sum(algorithm_location_urls, [])


# ------- MAIN -------
async def run():
    session = HttpSession()
    session.default_headers = HEADERS

    log.info('Starting "Geeks for Geeks" algorithms extraction')
    algorithms_urls = await follow_algorithms_urls(session)
    # algorithms_urls = [
    #     "https://www.geeksforgeeks.org/z-algorithm-linear-time-pattern-searching-algorithm/",
    # ]

    algorithms = await follow_algorithms(session, algorithms_urls)
    calculate_completition_rate(algorithms)

    return algorithms
