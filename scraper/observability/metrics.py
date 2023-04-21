import json

import matplotlib.pyplot as plt
import numpy
from mlxtend.plotting import plot_confusion_matrix

from scraper.schema import ScrapedAlgorithm
from scraper.utils import remove_duplicates, write_results_to_json


def make_results_caracterization(scraper: str) -> dict:
    with open(f"./results/{scraper}.json", "r") as file:
        file_contents = file.read()
        results = json.loads(file_contents)

    return {
        "Distinct Time Complexitys": len(
            list({algorithm["time_complexity"] for algorithm in results})
        ),
        "Distinct Space Complexitys": len(
            list({algorithm["space_complexity"] for algorithm in results})
        ),
        "Non Trusted Time Complexitys": len(
            [
                algorithm["trustable_time_complexity"]
                for algorithm in results
                if not algorithm["trustable_time_complexity"]
            ]
        ),
        "Non Trusted Space Complexitys": len(
            [
                algorithm["trustable_space_complexity"]
                for algorithm in results
                if not algorithm["trustable_space_complexity"]
            ]
        ),
    }


def make_completition_rate(scraper: str) -> dict:
    with open(f"./results/{scraper}.json", "r") as file:
        file_contents = file.read()
        results = json.loads(file_contents)

    total = len(results)
    time_complexity, space_complexity = 0, 0
    urls_with_problem = []

    for algorithm in results:
        if not algorithm["time_complexity"]:
            time_complexity += 1
        if not algorithm["space_complexity"]:
            space_complexity += 1
        if not algorithm["time_complexity"] or not algorithm["space_complexity"]:
            urls_with_problem.append(algorithm["url"])

    urls_with_problem = remove_duplicates(urls_with_problem)

    return {
        "Total Algorithms": total,
        "Time Complexity Extracted": f"{total - time_complexity} extracted - {100 - (time_complexity/total)*100}%",
        "Space Complexity Extraced": f"{total - space_complexity} extracted - {100 - (space_complexity/total)*100}%",
        "URLs with problem": urls_with_problem,
    }


def make_confusion_matrix(scraper: str) -> dict:
    with open(f"./results/manual_{scraper}.json", "r") as file:
        file_contents = file.read()
        manual_results = json.loads(file_contents)
    with open(f"./results/{scraper}.json", "r") as file:
        file_contents = file.read()
        results = json.loads(file_contents)

    (
        time_true_positive,
        time_false_positive,
        time_true_negative,
        time_false_negative,
    ) = (
        0,
        0,
        0,
        0,
    )

    (
        space_true_positive,
        space_false_positive,
        space_true_negative,
        space_false_negative,
    ) = (0, 0, 0, 0)

    for result, manual_result in zip(results, manual_results):
        if time_complexity := result["time_complexity"]:
            if time_complexity == manual_result["time_complexity"]:
                time_true_positive += 1
            else:
                time_false_positive += 1
        elif not result["time_complexity"]:
            if not manual_result["time_complexity"]:
                time_true_negative += 1
            else:
                time_false_negative += 1

        if space_complexity := result["space_complexity"]:
            if space_complexity == manual_result["space_complexity"]:
                space_true_positive += 1
            else:
                space_false_positive += 1
        elif not result["space_complexity"]:
            if not manual_result["space_complexity"]:
                space_true_negative += 1
            else:
                space_false_negative += 1

    time_accuracy = (time_true_positive + time_true_negative) / (
        time_true_positive
        + time_true_negative
        + time_false_positive
        + time_false_negative
    )
    time_precision = time_true_positive / (time_true_positive + time_false_positive)
    time_recall = time_true_positive / (time_true_positive + time_false_negative)
    time_f1_score = (2 * time_precision + time_recall) / (time_precision + time_recall)

    space_accuracy = (space_true_positive + space_true_negative) / (
        space_true_positive
        + space_true_negative
        + space_false_positive
        + space_false_negative
    )
    space_precision = space_true_positive / (space_true_positive + space_false_positive)
    space_recall = space_true_positive / (space_true_positive + space_false_negative)
    space_f1_score = (2 * space_precision + space_recall) / (
        space_precision + space_recall
    )

    # array = numpy.array(
    #     [
    #         [time_true_positive, time_false_negative],
    #         [time_false_positive, time_false_negative],
    #     ]
    # )
    # fig, ax = plot_confusion_matrix(conf_mat=array)
    # plt.title("Time Complexity Confusion Matrix")
    # plt.show()

    # array = numpy.array(
    #     [
    #         [space_true_positive, space_false_negative],
    #         [space_false_positive, space_false_negative],
    #     ]
    # )
    # fig, ax = plot_confusion_matrix(conf_mat=array)
    # plt.title("Space Complexity Confusion Matrix")
    # plt.show()

    return {
        "Time Complexity": {
            "True Positive": time_true_positive,
            "False Positive": time_false_positive,
            "True Negative": time_true_negative,
            "False negative": time_false_negative,
            "Accuracy": time_accuracy,
            "Precision": time_precision,
            "Recall": time_recall,
            "F1 Score": time_f1_score,
        },
        "Space Complexity": {
            "True Positive": space_true_positive,
            "False Positive": space_false_positive,
            "True Negative": space_true_negative,
            "False negative": space_false_negative,
            "Accuracy": space_accuracy,
            "Precision": space_precision,
            "Recall": space_recall,
            "F1 Score": space_f1_score,
        },
    }


def make_manual_results_boilerplate(scraper: str):
    with open(f"./results/{scraper}.json", "r") as file:
        file_contents = file.read()
        results = json.loads(file_contents)

    with open(f"./results/manual_{scraper}.txt", "w") as file:
        file.writelines(
            [
                f"{{'url' = {alg['url']}, 'time_complexity': ' ', 'space_complexity': ' '}}\n"
                for alg in results
            ]
        )


def make_results_analysis(scraper: str):
    write_results_to_json(
        f"./results/{scraper}_analysis",
        [
            {
                **make_completition_rate(scraper),
                **make_results_caracterization(scraper),
                **make_confusion_matrix(scraper),
            }
        ],
    )
