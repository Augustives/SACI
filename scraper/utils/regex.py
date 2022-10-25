import re

# COMPLEXITY_REGEX = (
#     r'O\(\w*\d+\)'
#     r'|O\(\w*\+\w+\)'
#     r'|O\(\w*\*\w*\(\w*\)\)'
# )

COMPLEXITY_REGEX = r'O\(.*?\)'


def re_search_complexity(text: str, pattern: str = COMPLEXITY_REGEX):
    match = re.search(pattern, text)
    if match:
        return match.group()
    else:
        return None


def re_all():
    ...
