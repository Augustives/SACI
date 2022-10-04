from aiohttp import ClientSession
from requests_html import AsyncHTMLSession
from re import match

from scraper.session.response import Response
from scraper.session.utils import (
    MissingMethodException, MissingArgumentException,
    InvalidUrlException, InvalidArgumentType,
    UnsupportedMethodException,
)
from scraper.session.settings import (
    REQUIRED_REQUEST_ARGS, REGEX, MAX_REDIRECTS
)


class HttpSession:
    def __init__(self):
        self._session = ClientSession()
        self._js_session = AsyncHTMLSession()
        self._headers = {}
        self._default_headers = {}

    @property
    def default_headers(self):
        return self._default_headers

    @default_headers.setter
    def default_headers(self, headers: dict):
        correct_type = dict
        if type(headers) != correct_type:
            raise InvalidArgumentType(correct_type)
        self._default_headers = headers

    @staticmethod
    def validate_url(url: str):
        if not match(REGEX['url'], url):
            raise InvalidUrlException

    def _validate_request_args(self, *args, **kwargs):
        method = kwargs.get('method')
        if not method:
            raise MissingMethodException
        elif method not in REQUIRED_REQUEST_ARGS.keys():
            raise UnsupportedMethodException
        else:
            for arg in REQUIRED_REQUEST_ARGS[method]:
                if not kwargs.get(arg):
                    raise MissingArgumentException(arg)

        self.validate_url(kwargs['url'])

        return kwargs

    def _make_headers(self, headers: dict):
        if not headers:
            return self._default_headers
        else:
            return {
                **self._default_headers
                ** headers
            }

    async def request(self, *args, **kwargs):
        self._validate_request_args(*args, **kwargs)
        callbacks = kwargs.pop('callbacks', None)

        response = await self._session.request(
            max_redirects=MAX_REDIRECTS,
            **{
                **kwargs,
                'headers': self._make_headers(kwargs.get('headers', {}))
            }
        )
        response = await Response.create_response_object(response)

        if callbacks:
            for callback in callbacks:
                response = callback(response)
        return response

    async def js_script_request(self, *args, **kwargs):
        self._validate_request_args(*args, **kwargs)
        script = kwargs.get('script')

        response = await self._js_session.request(kwargs)
        if script:
            return await response.html.arender(script=script)
        else:
            await response.html.arender()
            return response.html.full_text
