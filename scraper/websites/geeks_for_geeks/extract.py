from re import compile

from scraper.utils.regex import re_search_complexity


def method_1():
    def extract(response):
        complexitys = response.soup.find_all(
            string=compile(r'Time [Cc]omplexity[\s]?[:]+')
        )
        if not complexitys:
            return None
        complexitys = [
            complexity.find_previous('p').text
            for complexity in complexitys
            if 'Worst' not in complexity
        ]

        names = ''

        for complexity in complexitys:
            if 'Auxiliary' not in complexity:
                auxiliary_space = response.soup.find(
                    string=compile(r'Auxiliary Space[\s]?[:]+')
                )
                if not auxiliary_space:
                    auxiliary_space = ''
                auxiliary_space = auxiliary_space.find_previous('p').text

                return (
                    complexity +
                    auxiliary_space
                )

        return (
            complexity
        )

    def parse(raw_complexity):
        if 'Time' and 'Auxiliary' in raw_complexity:
            time, space = (
                re_search_complexity(complexity)
                for complexity in raw_complexity.split('Auxiliary')
            )
            complexity = {
                'time': time,
                'space': space
            }
        else:
            complexity = {
                'time': re_search_complexity(raw_complexity)
            }

        return complexity

    return extract, parse


EXTRACT_METHODS = [
    method_1()
]
