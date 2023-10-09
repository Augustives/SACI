class InvalidUrlException(Exception):
    def __init__(self, url):
        super().__init__(f"The provided URL '{url}' is not valid.")


class TooManyRetrysException(Exception):
    pass


class FailedExtraction(Exception):
    """Failed the extraction proccess"""

    pass


class FailedComplexityExtraction(Exception):
    """Failed to extract the complexitys"""

    pass
