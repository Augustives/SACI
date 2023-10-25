import json

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
