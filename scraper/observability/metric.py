from scraper.utils import remove_duplicates


def calculate_completition_rate(algorithms):
    total = len(algorithms)
    time_complexity, space_complexity = 0, 0
    urls_with_problem = []

    for algorithm in algorithms:
        if not algorithm["time_complexity"]:
            time_complexity += 1
        if not algorithm["space_complexity"]:
            space_complexity += 1
        if not algorithm["time_complexity"] or not algorithm["space_complexity"]:
            urls_with_problem.append(algorithm["url"])

    urls_with_problem = remove_duplicates(urls_with_problem)

    print(
        "##### RESULTS #####\n"
        f"Total={total}\n"
        f"Time Complexity={total - time_complexity}\n"
        f"Space Complexity={total - space_complexity}\n"
    )

    print(
        "##### ALGORITHMS WITH PROBLEM #####\n"
        f"Time Complexity={time_complexity}\n"
        f"Space Complexity={space_complexity}\n"
        f"Urls with problem:{urls_with_problem}\n"
    )
