from re import compile, search

from scraper.websites.geeks_for_geeks.settings import REGEX


# ------- COMMON -------
def extract_main_name(response):
    name = response.soup.find(
        'div', {'class': 'article-title'}
    )

    if name:
        return name.text
    return ''


def extract_time_complexity(complexity):
    match = search(REGEX['time_complexity'], complexity)
    if match:
        return match.group(1)
    return ''


def extract_auxiliary_space(complexity):
    match = search(REGEX['auxiliary_space'], complexity)
    if match:
        return match.group(1)
    return ''


def extract_code(code_table):
    ...


def parse_code(code_text):
    ...


# ------- METHODS -------
def method_1(response):
    name = extract_main_name(response)

    raw_complexitys = response.soup.find_all(
        string=compile(REGEX['complexity'])
    )
    raw_algorithms = [
        complexity.find_previous('td', {'class': 'code'})
        for complexity in raw_complexitys
    ]
    if not raw_complexitys or not raw_algorithms:
        return None

    complexitys = [
        complexity.find_previous('p').text
        for complexity in raw_complexitys
    ]
    algorithms = [
        parse_code(
            extract_code(algorithm)
        )
        for algorithm in raw_algorithms
    ]

    x = [
        {
            'name': name,
            'time_complexity': extract_time_complexity(complexity),
            'space_complexity': extract_auxiliary_space(complexity),
            'raw_algorithm': algorithm
        }
        for complexity in complexitys
        for algorithm in algorithms
    ]

    return x


EXTRACT_METHODS = [
    method_1
]
