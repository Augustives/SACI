from scraper.observability.metric import Metric

METRIC = Metric()

BASE_URL = 'https://www.geeksforgeeks.org'
ALGORITHMS_URL = f'{BASE_URL}/fundamentals-of-algorithms'

HEADERS = {
    'Host': 'www.geeksforgeeks.org',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',  # noqa
    'Accept-Encoding': 'gzip, deflate',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36',  # noqa

    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-User': '?1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Ch-Ua': '"Chromium";v="105", "Not)A;Brand";v="8"',
    'Sec-Ch-Ua-Mobile': '?0',
    'Sec-Ch-Ua-Platform': '"Windows"',
}


ALGORITHM_LINKS_JS_SCRIPT = """
    () => {
        const algorithm_links = []

        const ordered_lists = document.getElementsByTagName('ol');
        for (ol of ordered_lists) {
            const hrefs = []
            const a_tags = ol.getElementsByTagName('a')
            for (a of a_tags) {
                hrefs.push(a.getAttribute('href'))
            }
            algorithm_links.push(hrefs)
        }

        return algorithm_links
    }
"""

REGEX = {
    'time': r'Time [Cc]omplexity[\s]?[:]+',
    'auxiliary': r'Auxiliary [Ss]pace[\s]?[:]+',
    'time_complexity': r'Time [Cc]omplexity[\s]?[:]+\s*.*?(O\s*\(.*?\))',
    'auxiliary_space': r'Auxiliary [Ss]pace[\s]?[\[Cc\]omplexity]*[:]+\s*.*?(O\s*\(.*?\))'  # noqa
}


LANGUAGES = [
    'C',
    'C#',
    'C++',
    'Python3',
    'PHP',
    'Java',
    'Javascript'
]


SYMBOL_TABLE = {
    '\u221a': '√',

}
