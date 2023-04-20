import json

import matplotlib.pyplot as plt
import numpy
from mlxtend.plotting import plot_confusion_matrix

from scraper.utils import write_results_to_json


def make_manual_results_boilerplate():
    with open("./geeks_for_geeks.json", "r") as file:
        file_contents = file.read()
        results = json.loads(file_contents)

    with open("./urls.txt", "w") as file:
        file.writelines(
            [
                f"{{'url' = {alg['url']}, 'time_complexity': ' ', 'space_complexity': ' '}}\n"
                for alg in results
            ]
        )


def make_confusion_matrix():
    with open("./manual_results.json", "r") as file:
        file_contents = file.read()
        manual_results = json.loads(file_contents)
    with open("./geeks_for_geeks.json", "r") as file:
        file_contents = file.read()
        results = json.loads(file_contents)

    actual_time = [result["time_complexity"] for result in manual_results]
    scraped_time = [result["time_complexity"] for result in results]
    actual_space = [result["space_complexity"] for result in manual_results]
    scraped_space = [result["space_complexity"] for result in results]

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

    array = numpy.array(
        [
            [time_true_positive, time_false_negative],
            [time_false_positive, time_false_negative],
        ]
    )
    fig, ax = plot_confusion_matrix(conf_mat=array)
    plt.title("Time Complexity Confusion Matrix")
    plt.show()

    array = numpy.array(
        [
            [space_true_positive, space_false_negative],
            [space_false_positive, space_false_negative],
        ]
    )
    fig, ax = plot_confusion_matrix(conf_mat=array)
    plt.title("Space Complexity Confusion Matrix")
    plt.show()

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


if __name__ == "__main__":
    write_results_to_json("confusion_matrix", make_confusion_matrix())
