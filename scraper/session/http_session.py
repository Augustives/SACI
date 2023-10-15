import asyncio
import inspect

from aiohttp import ClientSession
from requests_html import AsyncHTMLSession
from yarl import URL

from scraper.exceptions import TooManyRetrysException
from scraper.observability.log import session_log as log
from scraper.session.exceptions import (
    InvalidArgumentType,
    InvalidUrlException,
    MissingArgumentException,
    MissingMethodException,
    UnsupportedMethodException,
)
from scraper.session.response import Response
from scraper.session.settings import MAX_REDIRECTS, REQUIRED_REQUEST_ARGS
from scraper.utils import retry


class HttpSession:
    def __init__(self):
        self._session = ClientSession()
        self._js_session = AsyncHTMLSession()
        self._default_headers = {}

    @property
    def default_headers(self):
        return self._default_headers

    @default_headers.setter
    def default_headers(self, headers: dict):
        if not isinstance(headers, dict):
            raise InvalidArgumentType(dict)
        self._default_headers = headers

    @staticmethod
    def validate_url(url: str):
        if not URL(url).is_absolute():
            raise InvalidUrlException(url)

    def _validate_request_args(self, **kwargs):
        method = kwargs.get("method")
        if not method:
            raise MissingMethodException
        if method not in REQUIRED_REQUEST_ARGS:
            raise UnsupportedMethodException
        for arg in REQUIRED_REQUEST_ARGS[method]:
            if arg not in kwargs:
                raise MissingArgumentException(arg)
        self.validate_url(kwargs["url"])

    def _make_headers(self, headers: dict) -> dict:
        return {**self._default_headers, **(headers or {})}

    @retry(times=3)
    async def _http_request(self, **kwargs):
        response = await self._session.request(
            max_redirects=MAX_REDIRECTS,
            **kwargs,
            headers=self._make_headers(kwargs.get("headers")),
        )
        await asyncio.sleep(2)
        return response

    async def request(self, **kwargs) -> Response:
        self._validate_request_args(**kwargs)
        callbacks = kwargs.pop("callbacks", None)

        try:
            aiohttp_response = await self._http_request(**kwargs)
        except TooManyRetrysException:
            log.error(f'Request failed. URL: {kwargs["url"]}')
            return Response()

        response = await Response.create_response_object(aiohttp_response)

        if callbacks:
            for callback in callbacks:
                if inspect.iscoroutinefunction(callback):
                    response = await callback(response)
                else:
                    response = callback(response)

        return response

    async def js_script_request(self, **kwargs):
        self._validate_request_args(**kwargs)
        script = kwargs.get("script")

        response = await self._js_session.request(kwargs)
        if script:
            return await response.html.arender(script=script)
        else:
            await response.html.arender()
            return response.html.full_text
