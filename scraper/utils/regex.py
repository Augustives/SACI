import re


# COMPLEXITY_REGEX = (
#     r'O\(\w*\d+\)'
#     r'|O\(\w*\+\w+\)'
#     r'|O\(\w*\*\w*\(\w*\)\)'
# )

COMPLEXITY_REGEX = r'O\(.*?\)'


def search(patter: str, text: str):
    ...
