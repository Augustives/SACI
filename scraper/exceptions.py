class TooManyRetrysException(Exception):
    pass


class FailedExtraction(Exception):
    """Failed the extraction proccess"""

    pass


class FailedTimeComplexityExtraction(Exception):
    """Failed to extract the time complexity"""

    pass


class FailedSpaceComplexityExtraction(Exception):
    """Failed to extract the space complexity"""

    pass
