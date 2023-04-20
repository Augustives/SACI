from scraper.schema import ScrapedAlgorithm
from scraper.utils import remove_duplicates, write_results_to_json


def make_results_caracterization(data: list[ScrapedAlgorithm]) -> dict:
    return {
        "Distinct Time Complexitys": len(
            list({algorithm.time_complexity for algorithm in data})
        ),
        "Distinct Space Complexitys": len(
            list({algorithm.space_complexity for algorithm in data})
        ),
        "Non Trusted Time Complexitys": len(
            [
                algorithm.trustable_time_complexity
                for algorithm in data
                if not algorithm.trustable_time_complexity
            ]
        ),
        "Non Trusted Space Complexitys": len(
            [
                algorithm.trustable_space_complexity
                for algorithm in data
                if not algorithm.trustable_space_complexity
            ]
        ),
    }


def make_completition_rate(data: list[ScrapedAlgorithm]) -> dict:
    total = len(data)
    time_complexity, space_complexity = 0, 0
    urls_with_problem = []

    for algorithm in data:
        if not algorithm.time_complexity:
            time_complexity += 1
        if not algorithm.space_complexity:
            space_complexity += 1
        if not algorithm.time_complexity or not algorithm.space_complexity:
            urls_with_problem.append(algorithm.url)

    urls_with_problem = remove_duplicates(urls_with_problem)

    return {
        "Total Algorithms": total,
        "Time Complexity Extracted": f"{total - time_complexity} extracted - {100 - (time_complexity/total)*100}%",
        "Space Complexity Extraced": f"{total - space_complexity} extracted - {100 - (space_complexity/total)*100}%",
        "URLs with problem": urls_with_problem,
    }


def make_results_analysis(data: list[ScrapedAlgorithm]):
    write_results_to_json(
        "results_analysis",
        [{**make_completition_rate(data), **make_results_caracterization(data)}],
    )
