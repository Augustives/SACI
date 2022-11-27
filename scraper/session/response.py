from aiohttp import ClientResponse
from bs4 import BeautifulSoup
from lxml import etree


class Response:
    def __init__(self, *args, **kwargs):
        self.url = kwargs.get("url")
        self.status = kwargs.get("status")
        self.content = kwargs.get("content")
        self.headers = kwargs.get("headers")
        self.original_response = kwargs.get("original_response")

        self.soup = kwargs.get("soup")

    @classmethod
    async def create_response_object(cls, aiohttp_response: ClientResponse):
        content = await aiohttp_response.text()

        kwargs = {
            "url": aiohttp_response.url,
            "status": aiohttp_response.status,
            "headers": aiohttp_response.headers,
            "content": content,
            "original_response": aiohttp_response,
            "soup": BeautifulSoup(content, "html.parser"),
        }

        return cls(**kwargs)

    def xptah(self, xpath_selector: str):
        htmlparser = etree.HTMLParser()
        tree = etree.parse(self.content, htmlparser)
        return tree.xpath(xpath_selector)
