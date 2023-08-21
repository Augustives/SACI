from aiohttp import ClientResponse
from bs4 import BeautifulSoup


class Response:
    def __init__(
        self,
        url: str,
        status: int,
        content: str,
        headers: dict,
        original_response: ClientResponse,
        soup: BeautifulSoup = None,
    ):
        self.url = url
        self.status = status
        self.content = content
        self.headers = headers
        self.original_response = original_response
        self.soup = soup or BeautifulSoup(content, "html.parser")
        self._tree = None

    @classmethod
    async def create_response_object(cls, aiohttp_response: ClientResponse):
        content = await aiohttp_response.text()

        return cls(
            url=aiohttp_response.url,
            status=aiohttp_response.status,
            headers=aiohttp_response.headers,
            content=content,
            original_response=aiohttp_response,
        )
