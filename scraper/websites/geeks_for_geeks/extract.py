from re import IGNORECASE, compile, search

from bs4.element import NavigableString, ResultSet, Tag

from scraper.exceptions import (
    FailedSpaceComplexityExtraction,
    FailedTimeComplexityExtraction,
)
from scraper.observability.log import scraper_log as log
from scraper.session.response import Response
from scraper.websites.geeks_for_geeks.settings import (
    AUXILIARY_SPACE_REGEX,
    COMMENTS_STARTING_STRINGS,
    HTML_ELEMENTS_NAMES,
    LANGUAGES,
    TIME_COMPLEXITY_REGEX,
)


# ------- FALLBACK METHODS -------
def time_complexity_fallback(reference_search_results: list[Tag]) -> str:
    for result in reference_search_results:
        if search(r"time", result, flags=IGNORECASE):
            time_complexity = search(TIME_COMPLEXITY_REGEX["fallback"], result).group()
            if time_complexity:
                return time_complexity


def space_complexity_fallback(reference_search_results: list[Tag]) -> str:
    for result in reference_search_results:
        if search(r"auxiliary|space", result, flags=IGNORECASE):
            auxiliary_space = search(TIME_COMPLEXITY_REGEX["fallback"], result).group()
            if auxiliary_space:
                return auxiliary_space


def extract_complexitys_fallback(dom_reference: Tag) -> tuple[str, str]:
    next_reference_search_results = [
        p.text
        for p in dom_reference.find_all_next("p")
        if search(TIME_COMPLEXITY_REGEX["fallback"], p.text)
    ]
    previous_reference_search_results = [
        p.text
        for p in dom_reference.find_all_previous("p")
        if search(TIME_COMPLEXITY_REGEX["fallback"], p.text)
    ]

    time_complexity = time_complexity_fallback(
        next_reference_search_results
    ) or time_complexity_fallback(previous_reference_search_results)
    space_complexity = space_complexity_fallback(
        next_reference_search_results
    ) or space_complexity_fallback(previous_reference_search_results)

    return time_complexity, space_complexity


# ------- EXTRACT METHODS -------
def extract_main_name(response: Response):
    name = response.soup.find("div", {"class": "article-title"})
    if name:
        return name.text


def extract_time_complexity_word(dom_reference: Tag) -> NavigableString:
    for regex in TIME_COMPLEXITY_REGEX["word"]:
        time_complexity_word = dom_reference.find_next(string=compile(regex))
        if time_complexity_word:
            return time_complexity_word


def extract_time_complexity(dom_reference: Tag) -> str:
    if time_complexity_word := extract_time_complexity_word(dom_reference):
        for regex in TIME_COMPLEXITY_REGEX["value"]:
            for element in HTML_ELEMENTS_NAMES:
                regex_match = search(
                    regex, time_complexity_word.find_previous(element).text
                )
                if regex_match:
                    return regex_match.group(1)
    raise FailedTimeComplexityExtraction


def extract_auxiliary_space_word(dom_reference: Tag) -> NavigableString:
    for regex in AUXILIARY_SPACE_REGEX["word"]:
        auxiliary_space_word = dom_reference.find_next(string=compile(regex))
        if auxiliary_space_word:
            return auxiliary_space_word


def extract_auxiliary_space(dom_reference: Tag) -> str:
    if auxiliary_space_word := extract_auxiliary_space_word(dom_reference):
        for regex in AUXILIARY_SPACE_REGEX["value"]:
            for element in HTML_ELEMENTS_NAMES:
                regex_match = search(
                    regex, auxiliary_space_word.find_previous(element).text
                )
                if regex_match:
                    return regex_match.group(1)
    raise FailedSpaceComplexityExtraction


def extract_code(code_table: Tag):
    code_text = ""
    code_lines = code_table.find_all("div", {"class": "line"})
    for line in code_lines:
        code_pieces = line.find_all("code")
        for code in code_pieces:
            code_text += code.text
        code_text += "\n"
    return code_text


def extract_code_comments(algorithm: str):
    algorithm_comments = ""
    for line in algorithm.splitlines():
        if line[:2] in COMMENTS_STARTING_STRINGS:
            algorithm_comments += line
            algorithm_comments += "\n"
        else:
            return algorithm_comments


# ------- SEARCH METHODS -------
def look_for_codes(response: Response) -> tuple[list, list]:
    codes, dom_references = [], []

    code_tabs = response.soup.find_all("div", {"class": "responsive-tabs"})
    for tab in code_tabs:
        languages_codes = {}
        dom_references.append(tab)

        for language in LANGUAGES:
            algorithm = tab.find_next("h2", {"class": "tabtitle"}, string=f"{language}")

            if algorithm:
                code = extract_code(algorithm.find_next("td", {"class": "code"}))

                languages_codes[language] = {
                    "code": code,
                    "comments": extract_code_comments(code),
                }

        codes.append(languages_codes)

    return codes, dom_references


def look_for_complexity(dom_reference: Tag) -> dict:
    trustable_time_complexity, trustable_space_complexity = True, True

    try:
        time_complexity = extract_time_complexity(dom_reference)
    except FailedTimeComplexityExtraction:
        trustable_time_complexity = False
        time_complexity, _ = extract_complexitys_fallback(dom_reference)

    try:
        space_complexity = extract_auxiliary_space(dom_reference)
    except FailedSpaceComplexityExtraction:
        trustable_space_complexity = False
        _, space_complexity = extract_complexitys_fallback(dom_reference)

    return {
        "time_complexity": time_complexity,
        "trustable_time_complexity": trustable_time_complexity,
        "space_complexity": space_complexity,
        "trustable_space_complexity": trustable_space_complexity,
    }


def look_for_names(dom_reference: Tag, response: Response):
    name = dom_reference.find_previous("h2")
    if not name or "tabtitle" in name.get("class", ""):
        return extract_main_name(response)
    return name.text


# ------- EXTRACT -------
def extract(response: Response) -> list:
    codes, dom_references = look_for_codes(response)
    if not codes:
        log.warning("Failed to find codes. " f"URL: {response.url}")
        return []

    complexitys = [
        look_for_complexity(dom_reference) for dom_reference in dom_references
    ]
    if not complexitys:
        log.error("Failed to find complexitys. " f"URL: {response.url}")
        return []

    names = [extract_main_name(response)] + [
        look_for_names(dom_reference, response) for dom_reference in dom_references[1:]
    ]

    return [
        {
            "name": name,
            "time_complexity": complexity.get("time_complexity"),
            "trustable_time_complexity": complexity.get("trustable_time_complexity"),
            "space_complexity": complexity.get("space_complexity"),
            "trustable_space_complexity": complexity.get("trustable_space_complexity"),
            "url": f"{response.url}",
            "codes": code,
        }
        for name, complexity, code in zip(names, complexitys, codes)
    ]
