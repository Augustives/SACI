from re import IGNORECASE, compile, search
from typing import Dict, List, Optional, Tuple, Union

from bs4.element import Tag

from scraper.exceptions import (
    FailedComplexityExtraction,
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


def get_sourceline(element):
    return element.sourceline if isinstance(element, Tag) else element.parent.sourceline


def search_regex(pattern: str, text: str, group_num: int = 0) -> Optional[str]:
    match = search(pattern, text)
    return match.group(group_num) if match else None


def extract_code(code_table: Tag) -> str:
    code_text = ""
    code_lines = code_table.find_all("div", {"class": "line"})
    for line in code_lines:
        code_pieces = line.find_all("code")
        for code in code_pieces:
            code_text += code.text
        code_text += "\n"
    return code_text


def extract_code_comments(algorithm: str) -> str:
    algorithm_comments = ""
    for line in algorithm.splitlines():
        if line[:2] in COMMENTS_STARTING_STRINGS:
            algorithm_comments += line
            algorithm_comments += "\n"
        else:
            return algorithm_comments


def extract_complexity_from_reference(
    reference: Tag, regex_map: Dict[str, List[str]]
) -> str:
    matches = [
        reference.find_next(string=compile(regex)) for regex in regex_map["word"]
    ]

    matches = [match for match in matches if match]

    closest_match = min(
        matches,
        key=lambda match: abs(get_sourceline(reference) - get_sourceline(match)),
    )

    for regex in regex_map["value"]:
        for element in HTML_ELEMENTS_NAMES:
            complexity = search_regex(
                regex, closest_match.find_previous(element).text, 1
            )
            if complexity:
                return complexity

    raise FailedComplexityExtraction


def extract_name(dom_reference: Tag) -> str:
    name = dom_reference.find_previous("h2")
    if name and "tabtitle" not in name.get("class", ""):
        return name.text


def fallback_search(reference_list: List[str], pattern: str) -> Optional[str]:
    for result in reference_list:
        if search(pattern, result, flags=IGNORECASE):
            return search_regex(TIME_COMPLEXITY_REGEX["fallback"], result)
    return None


def extract_complexity_with_fallback(
    dom_reference: Tag,
) -> Tuple[Optional[str], Optional[str]]:
    search_func = lambda x: search_regex(TIME_COMPLEXITY_REGEX["fallback"], x.text)
    next_results = [p.text for p in dom_reference.find_all_next("p") if search_func(p)]
    prev_results = [
        p.text for p in dom_reference.find_all_previous("p") if search_func(p)
    ]

    time_complexity = fallback_search(next_results, r"time") or fallback_search(
        prev_results, r"time"
    )
    space_complexity = fallback_search(
        next_results, r"auxiliary|space"
    ) or fallback_search(prev_results, r"auxiliary|space")

    return time_complexity, space_complexity


def extract_codes_and_references(
    response: Response,
) -> Tuple[List[Dict[str, str]], List[Tag]]:
    codes, references = [], []
    code_tabs = response.soup.find_all("div", {"class": "responsive-tabs"})

    for tab in code_tabs:
        code_map = {}
        references.append(tab)

        for lang in LANGUAGES:
            algorithm = tab.find_next("h2", {"class": "tabtitle"}, string=lang)
            if algorithm:
                code = extract_code(algorithm.find_next("td", {"class": "code"}))
                comments = extract_code_comments(code)

                code_map[lang] = {
                    "code": code,
                    "comments": comments,
                }

        codes.append(code_map)

    return codes, references


def extract_data(
    response: Response,
) -> List[Dict[str, Union[str, bool, Dict[str, str]]]]:
    codes, dom_references = extract_codes_and_references(response)
    if not codes:
        log.warning(f"Failed to find codes. URL: {response.url}")
        return []

    complexities = []
    for ref in dom_references:
        try:
            time_complexity = extract_complexity_from_reference(
                ref, TIME_COMPLEXITY_REGEX
            )
        except FailedComplexityExtraction:
            time_complexity, _ = extract_complexity_with_fallback(ref)

        try:
            space_complexity = extract_complexity_from_reference(
                ref, AUXILIARY_SPACE_REGEX
            )
        except FailedComplexityExtraction:
            _, space_complexity = extract_complexity_with_fallback(ref)

        complexities.append(
            {
                "time_complexity": time_complexity,
                "trustable_time_complexity": bool(time_complexity),
                "space_complexity": space_complexity,
                "trustable_space_complexity": bool(space_complexity),
            }
        )

    main_name = response.soup.find("div", {"class": "article-title"}).text
    names = [main_name] + [
        extract_name(ref) if extract_name(ref) else main_name
        for ref in dom_references[1:]
    ]

    return [
        {
            "name": name,
            "time_complexity": complexity["time_complexity"],
            "trustable_time_complexity": complexity["trustable_time_complexity"],
            "space_complexity": complexity["space_complexity"],
            "trustable_space_complexity": complexity["trustable_space_complexity"],
            "url": str(response.url),
            "codes": code,
        }
        for name, complexity, code in zip(names, complexities, codes)
    ]
