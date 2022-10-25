from asyncio import gather

from scraper.logger.log import scraper_log as log
from scraper.schema.json_schemas import ALGORITHM
from scraper.schema.schema import Schema
from scraper.session.http_session import HttpSession
from scraper.session.response import Response
from scraper.session.utils import Methods
from scraper.websites.geeks_for_geeks.extract import EXTRACT_METHODS
from scraper.websites.geeks_for_geeks.settings import ALGORITHMS_URL, HEADERS


# ------- VALIDATORS -------
def validate_algorithm_data(algorithm_data: dict):
    for key, value in algorithm_data.items():
        if not value:
            log.error(f'Failed to extract {key}')


# ------- PARSERS -------
def parse_algorithm_schema(algorithm_data: dict):
    algorithm_schema = Schema(
        algorithm_data, ALGORITHM
    )

    return algorithm_schema.validate()


# ------- FILTERS -------
def filter_algorithms_urls(alorithms_urls: list):
    return list(
        filter(
            lambda href: ('geeksquiz' not in href),
            alorithms_urls
        )
    )


# ------- EXTRACTORS -------
def extract_algorithm_data(response: Response):
    for extract, parse in EXTRACT_METHODS:
        raw_data = extract(response)

        if raw_data:
            return parse(raw_data)

    # return {
    #     'name': '',
    #     'time_complexity': data.get('time', ''),
    #     'space_complexity': data.get('space', ''),
    #     'raw_algorithm': ''
    # }


def extract_algorithms_urls(response: Response):
    page_content = response.soup.find(
        'div', {'class': 'page_content'}
    )

    return list(
        filter(
            None,
            [
                a.attrs.get('href')
                for ol in page_content.find_all('ol')[1:]
                for a in ol.find_all('a')
            ]
        )
    )


# ------- FOLLOWS -------
async def follow_algorithms(session: HttpSession, algorithms_urls: list):
    return await gather(
        *[
            session.request(
                method=Methods.GET.value,
                url=url,
                callbacks=[
                    extract_algorithm_data,
                    validate_algorithm_data
                ]
            )
            for url in algorithms_urls
        ]
    )


async def follow_algorithms_urls(session: HttpSession):
    return await session.request(
        method=Methods.GET.value,
        url=ALGORITHMS_URL,
        callbacks=[
            extract_algorithms_urls,
            filter_algorithms_urls
        ]
    )


async def run():
    session = HttpSession()
    session.default_headers = HEADERS

    log.info('Starting "Geeks for Geeks" algorithms extraction')
    algorithms_urls = await follow_algorithms_urls(session)
    algorithms_data = await follow_algorithms(session, algorithms_urls)
    algorithms_schema = [
        parse_algorithm_schema(algorithm_data)
        for algorithm_data in algorithms_data
    ]

    return algorithms_schema
