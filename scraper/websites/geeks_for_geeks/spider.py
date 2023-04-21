from asyncio import gather

from scraper.exceptions import FailedExtraction
from scraper.observability.log import scraper_log as log
from scraper.observability.metrics import make_results_analysis
from scraper.schema import ScrapedAlgorithm
from scraper.session.http_session import HttpSession
from scraper.session.response import Response
from scraper.session.utils import Methods
from scraper.utils import remove_duplicates, retry
from scraper.websites.geeks_for_geeks.extract import extract
from scraper.websites.geeks_for_geeks.login import follow_login
from scraper.websites.geeks_for_geeks.settings import ALGORITHMS_LOCATION_URLS, HEADERS


# ------- PARSERS -------
def parse_algorithm_schema(algorithms_data: list) -> list:
    return [ScrapedAlgorithm(**algorithm) for algorithm in algorithms_data]


# ------- FILTERS -------
def filter_algorithms_urls(alorithms_urls: list) -> list:
    return list(filter(lambda href: ("geeksquiz" not in href), alorithms_urls))


# ------- EXTRACTORS -------
def extract_algorithm_data(response: Response) -> list:
    if response:
        data = extract(response)
        if data:
            return data
        else:
            raise FailedExtraction
    return []


def extract_algorithms_urls(response: Response) -> list:
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
@retry(times=3, raise_exception=False, return_value=[])
async def follow_algorithm(session: HttpSession, url: str):
    return await session.request(
        method=Methods.GET.value,
        url=url,
        callbacks=[extract_algorithm_data, parse_algorithm_schema],
    )


async def follow_algorithms(session: HttpSession, algorithms_urls: list) -> list:
    algorithms = await gather(
        *[follow_algorithm(session, url) for url in algorithms_urls]
    )
    return sum(algorithms, [])


async def follow_algorithms_urls(session: HttpSession) -> list:
    algorithm_location_urls = await gather(
        *[
            session.request(
                method=Methods.GET.value,
                url=url,
                callbacks=[
                    extract_algorithms_urls,
                    filter_algorithms_urls,
                    remove_duplicates,
                ],
            )
            for url in ALGORITHMS_LOCATION_URLS
        ]
    )
    return sum(algorithm_location_urls, [])


# ------- RUN -------
async def run(url: str = None) -> list:
    session = HttpSession()
    session.default_headers = HEADERS

    log.info('Starting "Geeks for Geeks" algorithms extraction')
    if not url:
        algorithms_urls = await follow_algorithms_urls(session)
    else:
        algorithms_urls = [url]

    await follow_login(session)
    algorithms = await follow_algorithms(session, algorithms_urls)

    return algorithms
