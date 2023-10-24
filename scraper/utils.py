import json
import os

from asyncio_throttle import Throttler
from langchain.chains import LLMChain
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate

from scraper.exceptions import TooManyRetrysException
from scraper.observability.log import scraper_log as log


def retry(
    times: int,
    raise_exception=True,
    return_value=None,
):
    def func_wrapper(f):
        async def wrapper(*args, **kwargs):
            for _ in range(times):
                try:
                    return await f(*args, **kwargs)
                except Exception:
                    pass

            if not raise_exception:
                return return_value
            else:
                raise TooManyRetrysException

        return wrapper

    return func_wrapper


def remove_duplicates(data: list) -> list:
    return list(set(data))


def open_results_from_json(file_path: str) -> dict:
    with open(file_path, "r") as file:
        file_contents = file.read()
        results = json.loads(file_contents)
    return results


def write_results_to_json(file_path: str, data: list):
    with open(f"{file_path}.json", "w") as file:
        json.dump(data, file)


class LlmComplexitySearcher:
    _instance = None
    throttler = Throttler(rate_limit=100, period=60)

    def __init__(self):
        self.LLM = OpenAI(openai_api_key=os.environ.get("OPENAI_KEY", ""))
        self.PROMPT = PromptTemplate.from_template(
            """I am using you during a scraping operation which I need to extract from text the values of complexity.
            Consider that sometimes the space complexity is also called as auxiliary space.
            Consider that both complexitys often come in this format: 'Some type of complexity: value of complexity'.
            But they can also come inside the text like: 'The type of complexity of the given ... is ...'.
            Give the answer in JSON format with no line breaks, with a key called "complexity" and the value for the key is your answer.
            If you cant determine the answer give the json with a null in the value.
            What is the {complexity} that is written in the following text: "{text}"?"""
        )
        self.LLM_CHAIN = LLMChain(prompt=self.PROMPT, llm=self.LLM)

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    @retry(times=3, raise_exception=False, return_value={"complexity": None})
    async def search(self, complexity: str, text: str) -> dict:
        async with self.throttler:
            answer = self.LLM_CHAIN.run(complexity=complexity, text=text)
            return json.loads(answer)
