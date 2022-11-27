def calculate_completition_rate(algorithms):
    time_complexity = 0
    space_complexity = 0

    for algorithm in algorithms:
        if algorithm["time_complexity"]:
            time_complexity += 1
        if algorithm["space_complexity"]:
            space_complexity += 1

    return print(
        "##### RESULTS #####\n"
        f"Total={len(algorithms)}\n"
        f"Time Complexity={time_complexity}\n"
        f"Space Complexity={space_complexity}\n"
    )
