from base64 import b64encode
from re import compile, search

from scraper.observability.log import scraper_log as log
from scraper.websites.geeks_for_geeks.settings import LANGUAGES, REGEX


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


def extract_algorithm(code_table):
    code_text = ""
    code_lines = code_table.find_all('div', {'class': 'line'})
    for line in code_lines:
        code_pieces = line.find_all('code')
        for code in code_pieces:
            code_text += code.text
        code_text += '\n'
    return code_text


def extract_algorithm_comments(algorithm):
    algorithm_comments = ''
    for line in algorithm.splitlines():
        if line[:2] in ['//', '# ']:
            algorithm_comments += line
            algorithm_comments += '\n'
        else:
            return algorithm_comments


# ------- SEARCH METHODS -------
def look_for_algorithms(response):
    algorithms = []
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
                code = extract_algorithm(
                    algorithm.find_next(
                        'td', {'class': 'code'}
                    )
                )

                languages_algorithms[language] = {
                    'code': parse_code(code),
                    'comments': extract_algorithm_comments(code)
                }

        algorithms.append(languages_algorithms)

    return algorithms, dom_references


def look_for_complexity(dom_reference):
    complexity = dom_reference.find_next(
        string=compile(REGEX['time'])
    )
    if not complexity:
        return {}
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


def look_for_names(dom_reference, response):
    name = dom_reference.find_previous('h2')
    if not name or 'tabtitle' in name.get('class', ''):
        return extract_main_name(response)
    return name.text


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
        log.warning(
            'Failed to find algorithms. '
            f'URL: {response.url}'
        )
        return []

    complexitys = [
        look_for_complexity(dom_reference)
        for dom_reference in dom_references
    ]
    if not complexitys:
        log.error(
            'Failed to find complexitys. '
            f'URL: {response.url}'
        )
        return []

    names = [
        look_for_names(dom_reference, response)
        for dom_reference in dom_references[1:]
    ]
    names.insert(0, extract_main_name(response))

    return [
        {
            'name': name,
            'time_complexity': complexity.get('time'),
            'space_complexity': complexity.get('space'),
            'url': f'{response.url}',
            'algorithm': algorithm,
        }
        for name, complexity, algorithm in
        zip(names, complexitys, algorithms)
    ]
