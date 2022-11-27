from enum import Enum


class Methods(Enum):
    GET = "get"
    POST = "post"


class InvalidUrlException(Exception):
    def __init__(self):
        self.message = "Please provide a valid URL string!"
        super().__init__(self.message)


class MissingMethodException(Exception):
    def __init__(self):
        self.message = "Please provide a request method!"
        super().__init__(self.message)


class UnsupportedMethodException(Exception):
    def __init__(self):
        self.message = "Please provide a supported method!"
        super().__init__(self.message)


class MissingArgumentException(Exception):
    def __init__(self, argument):
        self.message = f"Please provide the missing argument: {argument}!"
        super().__init__(self.message)


class InvalidArgumentType(Exception):
    def __init__(self, type):
        self.message = f"Please provide the correct argument type: {type}!"
        super().__init__(self.message)
