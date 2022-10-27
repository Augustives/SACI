from base64 import b64encode
from re import compile, search

from scraper.websites.geeks_for_geeks.settings import REGEX


# ------- EXTRACT METHODS -------
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


def look_for_auxiliary_space(complexity):
    if not extract_auxiliary_space(complexity):
        auxiliary_space = complexity.find_next(
            string=compile(REGEX['auxiliary'])
        )
        if auxiliary_space:
            return (
                complexity.find_previous('p').text +
                auxiliary_space.find_previous('p').text
            )
    return complexity.find_previous('p').text


def extract_code(code_table):
    code_text = ""
    code_lines = code_table.find_all('div', {'class': 'line'})
    for line in code_lines:
        code_pieces = line.find_all('code')
        for code in code_pieces:
            code_text += code.text
        code_text += '\n'
    return code_text


def parse_code(code_text):
    # TODO Parse the code in an understandable way, remove comments, etc
    return str(
        b64encode(code_text.encode())
    )


# ------- EXTRACT -------
def extract(response):
    name = extract_main_name(response)

    raw_complexitys = response.soup.find_all(
        string=compile(REGEX['time'])
    )

    raw_algorithms = []
    for complexity in raw_complexitys:
        python_algorithm = complexity.find_previous(
                'h2', {'class': 'tabtitle'},
                string=compile(r'Python')
            )
        if python_algorithm:
            raw_algorithms.append(
                python_algorithm.find_next(
                    'td', {'class': 'code'}
                )
            )

    if not raw_complexitys or not raw_algorithms:
        return []

    complexitys = [
        look_for_auxiliary_space(complexity)
        for complexity in raw_complexitys
    ]

    algorithms = [
        parse_code(
            extract_code(algorithm)
        )
        for algorithm in raw_algorithms
    ]

    return [
        {
            'name': name,
            'time_complexity': extract_time_complexity(complexity),
            'space_complexity': extract_auxiliary_space(complexity),
            'raw_algorithm': algorithm
        }
        for complexity, algorithm in zip(complexitys, algorithms)
    ]
