from asyncio import gather
from bs4 import BeautifulSoup

from scraper.logger import log
from scraper.session import HttpSession, Methods
from scraper.session.response import Response
from scraper.websites.geeks_for_geeks.settings import (
    HEADERS, ALGORITHMS_URL
)


def parse_algorithm():
    ...


def parse_algorithms():
    ...


def filter_algorithms_urls(alorithms_urls: list):
    return list(
        filter(
            lambda href: ('geeksquiz' not in href),
            alorithms_urls
        )
    )


def extract_algorithm_data():
    ...


def extract_algorithms_data(response: Response):
    return [

    ]


def extract_algorithms_urls(response: Response):
    soup = BeautifulSoup(response.content, 'html.parser')
    page_content = soup.find('div', {'class': 'page_content'})

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


async def follow_algorithms(session: HttpSession, algorithms_urls: list):
    return await gather(
        *[
            session.request(
                method=Methods.GET.value,
                url=url,
                callbacks=[extract_algorithms_data]
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


async def run(session: HttpSession):
    session = HttpSession()
    session.default_headers = HEADERS

    log.info('Starting "Geeks for Geeks" algorithms extraction')
    algorithms_urls = await follow_algorithms_urls(session)
    algorithms = await follow_algorithms(session, algorithms_urls)

    return algorithms
