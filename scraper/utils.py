import json

from scraper.exceptions import TooManyRetrysException
from scraper.observability.log import scraper_log as log
from scraper.settings import UNDESIRED_CHARACTERS


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


def clean_text_characters(text: str) -> str:
    for character in UNDESIRED_CHARACTERS:
        text = text.replace(character, "")
    return text


def remove_duplicates(data: list) -> list:
    return list(set(data))


def write_results_to_json(file_name: str, data: list):
    with open(f"./{file_name}.json", "w") as file:
        json.dump(data, file)
