import re
import requests
import math
from collections import Counter

import matplotlib.pyplot as plt
import numpy
from bs4 import BeautifulSoup
from mlxtend.plotting import plot_confusion_matrix

from scraper.utils import (
    open_results_from_json,
    remove_duplicates,
    write_results_to_json,
)


def make_results_caracterization(scraper: str) -> dict:
    results = open_results_from_json(f"./results/{scraper}.json")

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
    results = open_results_from_json(f"./results/{scraper}.json")

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
    manual_results = open_results_from_json(f"./results/manual_{scraper}.json")
    results = open_results_from_json(f"./results/{scraper}.json")

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
    time_f1_score = (2 * time_precision * time_recall) / (time_precision + time_recall)

    space_accuracy = (space_true_positive + space_true_negative) / (
        space_true_positive
        + space_true_negative
        + space_false_positive
        + space_false_negative
    )
    space_precision = space_true_positive / (space_true_positive + space_false_positive)
    space_recall = space_true_positive / (space_true_positive + space_false_negative)
    space_f1_score = (2 * space_precision * space_recall) / (
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
    results = open_results_from_json(f"./results/{scraper}.json")

    write_results_to_json(
        f"./results/manual_{scraper}",
        [
            {"url": alg["url"], "time_complexity": " ", "space_complexity": " "}
            for alg in results
        ],
    )


def make_complexitys_classification(scraper: str):
    results = open_results_from_json(f"./results/{scraper}.json")
    (
        time_constant,
        time_linear,
        time_exponential,
        time_polynomial,
        time_factorial,
        time_logarithmic,
    ) = (0, 0, 0, 0, 0, 0)
    (
        space_constant,
        space_linear,
        space_exponential,
        space_polynomial,
        space_factorial,
        space_logarithmic,
    ) = (0, 0, 0, 0, 0, 0)
    for result in results:
        if time_complexity := result["time_complexity"]:
            if re.match(r"O\(1\)", time_complexity):
                time_constant += 1
            elif re.match(r"O\(\w\)", time_complexity):
                time_linear += 1
            elif re.match(r"O\(.*!.*\)", time_complexity):
                time_factorial += 1
            elif re.match(r"O\(.*log.*\)", time_complexity):
                time_logarithmic += 1
            elif re.match(r"O\(\d\^?\w\)", time_complexity):
                time_exponential += 1
            elif re.match(
                r"O\(\w\s*[\^\*\+]?\s*[\d\w\s]+.*\)", time_complexity
            ) or re.match("O\(\d+\(\w\*\w\)", time_complexity):
                time_polynomial += 1

        if space_complexity := result["space_complexity"]:
            if re.match(r"O\(1\)", space_complexity):
                space_constant += 1
            elif re.match(r"O\(\w\)", space_complexity):
                space_linear += 1
            elif re.match(r"O\(.*!.*\)", space_complexity):
                space_factorial += 1
            elif re.match(r"O\(.*log.*\)", space_complexity):
                space_logarithmic += 1
            elif re.match(r"O\(\d\^?\w\)", space_complexity):
                space_exponential += 1
            elif re.match(
                r"O\(\w\s*[\^\*\+]?\s*[\d\w\s]+.*\)", space_complexity
            ) or re.match("O\(\d+\(\w\*\w\)", space_complexity):
                space_polynomial += 1

    return {
        "Time Complexity Classification": {
            "Constant complexity": time_constant,
            "Linear complexity": time_linear,
            "Exponential complexity": time_exponential,
            "Polynomial complexity": time_polynomial,
            "Factorial complexity": time_factorial,
            "Log complexity": time_logarithmic,
        },
        "Space Complexity Classification": {
            "Constant complexity": space_constant,
            "Linear complexity": space_linear,
            "Exponential complexity": space_exponential,
            "Polynomial complexity": space_polynomial,
            "Factorial complexity": space_factorial,
            "Log complexity": space_logarithmic,
        },
    }


def make_algorithms_histogram(scraper: str):
    results = open_results_from_json(f"./results/{scraper}.json")

    count = Counter([result["url"] for result in results]).values()
    plt.hist(count)
    plt.xlabel("Número de Algoritmos")
    plt.ylabel("Frequência")
    plt.title("Histograma da Distribuição de Algoritmos")
    plt.show()


def calculate_html_nodes_depth(scraper: str):
    def traverse_tree(node, depth):
        tag = node.name
        if tag not in depths:
            depths[tag] = []
        depths[tag].append(depth)

        if hasattr(node, "children"):
            for child in node.children:
                if hasattr(child, "name"):
                    traverse_tree(child, depth + 1)

    results = open_results_from_json(f"./results/{scraper}.json")
    urls = list(set([result["url"] for result in results]))

    all_max_depths, all_num_nodes = [], []
    for url in urls:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")

        depths = {}
        traverse_tree(soup, 0)

        max_depth = max([max(depths[tag]) for tag in depths])
        num_nodes = sum([len(depths[tag]) for tag in depths])

        all_max_depths.append(max_depth)
        all_num_nodes.append(num_nodes)

    _, axs = plt.subplots(1, 2, figsize=(10, 5))
    axs[0].hist(all_max_depths, bins=[23, 24, 25, 26])
    axs[0].set_xlabel("Profundidade Máxima")
    axs[0].set_ylabel("Frequência")
    axs[0].set_title("Histograma da Profundidade Máxima")

    axs[1].hist(all_num_nodes, bins=[2500, 7500, 12500, 17500, 22500, 30000])
    axs[1].set_xlabel("Número de Nodos")
    axs[1].set_ylabel("Frequência")
    axs[1].set_title("Histograma da Contagem de Nodos")

    plt.suptitle("Combined Histogram for All URLs")
    plt.show()


def make_results_analysis(scraper: str):
    write_results_to_json(
        f"./results/{scraper}_analysis",
        [
            {
                **make_completition_rate(scraper),
                **make_results_caracterization(scraper),
                **make_confusion_matrix(scraper),
                **make_complexitys_classification(scraper),
            }
        ],
    )
    # calculate_html_nodes_depth(scraper)
    # make_algorithms_histogram(scraper)
