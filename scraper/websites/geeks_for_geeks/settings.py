BASE_URL = "https://www.geeksforgeeks.org"

ALGORITHMS_LOCATION_URLS = [
    f"{BASE_URL}/fundamentals-of-algorithms",
    f"{BASE_URL}/data-structures",
]

HEADERS = {
    "Host": "www.geeksforgeeks.org",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Accept-Encoding": "gzip, deflate",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36",
    "Sec-Fetch-Site": "none",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-User": "?1",
    "Sec-Fetch-Dest": "document",
    "Sec-Ch-Ua": '"Chromium";v="105", "Not)A;Brand";v="8"',
    "Sec-Ch-Ua-Mobile": "?0",
    "Sec-Ch-Ua-Platform": '"Windows"',
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

TIME_COMPLEXITY_REGEX = {
    "word": [r"Time [Cc]omplexity[\s]?[:]?"],
    "value": [
        r"Time [Cc]omplexity[\s]?[:]+\s*.*?(O\s*\(.*?\))",
        r"Time [Cc]omplexity[\s]?[:]+\s*.*?time complexity.*?\sis\s(\w*)",
    ],
}

AUXILIARY_SPACE_REGEX = {
    "word": [r"Auxiliary [Ss]pace[\s]?[:]?", r"Space [Cc]omplexity[\s]?[:]?"],
    "value": [
        r"Auxiliary [Ss]pace[\s]?[\[Cc\]omplexity]*[:]+\s*.*?(O\s*\(.*?\))",
        r"Space [Cc]omplexity[\s]?[\[Cc\]omplexity]*[:]+\s*.*?(O\s*\(.*?\))",
    ],
}

HTML_ELEMENTS_NAMES = ["p", "li", "ul", "i"]

COMMENTS_STARTING_STRINGS = ["//", "# ", "/*"]

LANGUAGES = ["C", "C#", "C++", "Python3", "Python", "PHP", "Java", "Javascript"]
