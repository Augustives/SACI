from base64 import b64encode
from re import compile, search

from scraper.observability.log import scraper_log as log
from scraper.observability.metric import Stages
from scraper.websites.geeks_for_geeks.settings import LANGUAGES, METRIC, REGEX


# ------- EXTRACT METHODS -------
def extract_main_name(response):
    name = response.soup.find(
        'div', {'class': 'article-title'}
    )
    if name:
        return name.text
    return ''


@METRIC.decorator(Stages.TIME.value)
def extract_time_complexity(complexity):
    match = search(REGEX['time_complexity'], complexity)
    if match:
        return match.group(1)
    return ''


@METRIC.decorator(Stages.SPACE.value)
def extract_auxiliary_space(complexity):
    match = search(REGEX['auxiliary_space'], complexity)
    if match:
        return match.group(1)
    return ''


def extract_algorithm(code_table):
    code_text = ""
    code_lines = code_table.find_all('div', {'class': 'line'})
    for line in code_lines:
        code_pieces = line.find_all('code')
        for code in code_pieces:
            code_text += code.text
        code_text += '\n'
    return code_text


# ------- SEARCH METHODS -------
def look_for_algorithms(response):
    raw_algorithms = []
    dom_references = []

    algorithm_tabs = response.soup.find_all(
        'div', {'class': 'responsive-tabs'}
    )
    for tab in algorithm_tabs:
        languages_algorithms = {}
        dom_references.append(tab)

        for language in LANGUAGES:
            algorithm = tab.find_next(
                    'h2', {'class': 'tabtitle'},
                    string=f'{language}'
                )

            if algorithm:
                languages_algorithms[language] = parse_code(
                    extract_algorithm(
                        algorithm.find_next(
                            'td', {'class': 'code'}
                        )
                    )
                )

        raw_algorithms.append(languages_algorithms)

    return raw_algorithms, dom_references


def look_for_complexity(dom_reference):
    complexity = dom_reference.find_next(
        string=compile(REGEX['time'])
    )
    return look_for_auxiliary_space(complexity)


def look_for_auxiliary_space(complexity):
    complexitys = {
        'time': extract_time_complexity(
            complexity.find_previous('p').text
        )
    }

    if not extract_auxiliary_space(complexity):
        auxiliary_space = complexity.find_next(
            string=compile(REGEX['auxiliary'])
        )
        if auxiliary_space:
            complexitys['space'] = extract_auxiliary_space(
                auxiliary_space.find_previous('p').text
            )

    return complexitys


def look_for_name(dom_reference):

    ...


# ------- PARSE METHODS -------
def parse_code(code_text):
    # TODO Parse the code in an understandable way, remove comments, etc
    return str(
        b64encode(code_text.encode())
    )


# ------- EXTRACT -------
def extract(response):
    algorithms, dom_references = look_for_algorithms(response)
    if not algorithms:
        log.error(
            'Failed to find complexity or algorithms.'
            f'URL: {response.url}'
        )
        return None

    # TODO look_for_titles_function
    names = extract_main_name(response)

    complexitys = [
        look_for_complexity(dom_reference)
        for dom_reference in dom_references
    ]

    return [
        {
            'name': name,
            'time_complexity': complexity['time'],
            'space_complexity': complexity['space'],
            'raw_algorithm': algorithm
        }
        for name, complexity, algorithm in zip(names, complexitys, algorithms)
    ]
