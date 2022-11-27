AVAILABLE_METHODS = ["get", "post"]

REGEX = {
    "url": r"(https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9]+\.[^\s]{2,}|www\.[a-zA-Z0-9]+\.[^\s]{2,})"  # noqa
}

REQUIRED_REQUEST_ARGS = {"get": ["url"], "post": ["url", "data"]}

MAX_REDIRECTS = 5
