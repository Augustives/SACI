from scraper.utils import remove_duplicates
from scraper.utils import write_results_to_json
from scraper.schema import ScrapedAlgorithm


def results_caracterization(data: list[ScrapedAlgorithm]) -> dict:
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


def calculate_completition_rate(data: list[ScrapedAlgorithm]) -> dict:
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
        "Time Complexity Extracted": f"{total - time_complexity} extracted - {(time_complexity/total)*100}%",
        "Space Complexity Extraced": f"{total - space_complexity} extracted - {(space_complexity/total)*100}%",
        "URLs with problem": urls_with_problem,
    }


def make_results_analysis(data: list[ScrapedAlgorithm]):
    write_results_to_json(
        "results_analysis.json",
        [{**calculate_completition_rate(data), **results_caracterization(data)}],
    )
