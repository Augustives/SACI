from re import compile


def search_for_complexity(soup):
    complexity = soup.find(string=compile(r'Time Complexity[\s]?[:]+'))
    if complexity:
        return complexity.find_previous('p').text
    return ''


def search_for_auxiliary_space(soup):
    auxiliary_space = soup.find(string=compile(r'Auxiliary Space[\s]?[:]+'))
    if not auxiliary_space:
        return auxiliary_space.find_previous('p').text
    return ''


def method_1(soup):
    complexity = search_for_complexity(soup)
    if 'Auxiliary' not in complexity:
        auxiliary_space = search_for_auxiliary_space(soup)
    return (
        complexity +
        auxiliary_space
    )


EXTRACTION_METHODS = [
    method_1
]
