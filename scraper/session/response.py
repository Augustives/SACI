class Response:
    def __init__(self, *args, **kwargs):
        self.url = kwargs.get('url')
        self.status = kwargs.get('status')
        self.content = kwargs.get('content')
        self.json = kwargs.get('json')
        self.headers = kwargs.get('headers')
        self.original_response = kwargs.get('original_response')

    @classmethod
    async def create_response_object(cls, aiohttp_response):
        try:
            json = await aiohttp_response.json()
        except Exception:
            json = {}

        kwargs = {
            'url': aiohttp_response.url,
            'status': aiohttp_response.status,
            'content': await aiohttp_response.text(),
            'json': json,
            'headers': aiohttp_response.headers,
            'original_response': aiohttp_response
        }

        return cls(**kwargs)
