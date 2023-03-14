from base64 import b64encode
from re import compile, search

from bs4.element import NavigableString, Tag

from scraper.observability.log import scraper_log as log
from scraper.session.response import Response
from scraper.websites.geeks_for_geeks.settings import (
    AUXILIARY_SPACE_REGEX,
    COMMENTS_STARTING_STRINGS,
    HTML_ELEMENTS_NAMES,
    LANGUAGES,
    TIME_COMPLEXITY_REGEX,
)


# ------- EXTRACT METHODS -------
def extract_main_name(response: Response):
    name = response.soup.find("div", {"class": "article-title"})
    if name:
        return name.text


def extract_time_complexity_word(dom_reference: Tag) -> str:
    for regex in TIME_COMPLEXITY_REGEX["word"]:
        time_complexity_word = dom_reference.find_next(string=compile(regex))
        if time_complexity_word:
            return time_complexity_word


def extract_time_complexity(dom_reference: Tag) -> str:
    if time_complexity_word := extract_time_complexity_word(dom_reference):
        for regex in TIME_COMPLEXITY_REGEX["value"]:
            for element in HTML_ELEMENTS_NAMES:
                match = search(regex, time_complexity_word.find_previous(element).text)
                if match:
                    return match.group(1)


def extract_auxiliary_space_word(dom_reference: Tag) -> NavigableString:
    for regex in AUXILIARY_SPACE_REGEX["word"]:
        auxiliary_space_word = dom_reference.find_next(string=compile(regex))
        if auxiliary_space_word:
            return auxiliary_space_word


def extract_auxiliary_space(dom_reference: Tag) -> str:
    if auxiliary_space_word := extract_auxiliary_space_word(dom_reference):
        for regex in AUXILIARY_SPACE_REGEX["value"]:
            for element in HTML_ELEMENTS_NAMES:
                match = search(regex, auxiliary_space_word.find_previous(element).text)
                if match:
                    return match.group(1)


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
                    "code": parse_code(code),
                    "comments": extract_code_comments(code),
                }

        codes.append(languages_codes)

    return codes, dom_references


def look_for_complexity(dom_reference: Tag) -> dict:
    time_complexity = extract_time_complexity(dom_reference)
    space_complexity = extract_auxiliary_space(dom_reference)
    return {"time": time_complexity, "space": space_complexity}


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

    names = [
        look_for_names(dom_reference, response) for dom_reference in dom_references[1:]
    ]
    names.insert(0, extract_main_name(response))

    return [
        {
            "name": name,
            "time_complexity": complexity.get("time"),
            "space_complexity": complexity.get("space"),
            "url": f"{response.url}",
            "code": code,
        }
        for name, complexity, code in zip(names, complexitys, codes)
    ]
