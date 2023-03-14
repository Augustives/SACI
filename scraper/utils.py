from scraper.settings import UNDESIRED_CHARACTERS


class TooManyRetrysException(Exception):
    pass


def retry(times):
    def func_wrapper(f):
        async def wrapper(*args, **kwargs):
            for _ in range(times):
                try:
                    return await f(*args, **kwargs)
                except Exception:
                    pass
            raise TooManyRetrysException()

        return wrapper

    return func_wrapper


def clean_text_characters(text: str) -> str:
    for character in UNDESIRED_CHARACTERS:
        text = text.replace(character, "")
    return text
