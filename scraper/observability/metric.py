def calculate_completition_rate(algorithms):
    total = len(algorithms)
    time_complexity, space_complexity = 0, 0
    urls = []

    for algorithm in algorithms:
        if not algorithm["time_complexity"]:
            time_complexity += 1
        if not algorithm["space_complexity"]:
            space_complexity += 1
        if not algorithm["time_complexity"] or algorithm["space_complexity"]:
            urls.append(algorithm["url"])

    urls = list(set(urls))

    print(
        "##### RESULTS #####\n"
        f"Total={total}\n"
        f"Time Complexity={total - time_complexity}\n"
        f"Space Complexity={total - space_complexity}\n"
    )

    print("##### ALGORITHMS WITH PROBLEM #####\n" f"Total={len(urls)}\n" f"Urls={urls}")
