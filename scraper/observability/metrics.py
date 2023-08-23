import math
import re
from collections import Counter
from typing import Any, Dict, List, Tuple, Union

import matplotlib.pyplot as plt
import numpy
import requests
from bs4 import BeautifulSoup, NavigableString, Tag
from mlxtend.plotting import plot_confusion_matrix

from scraper.utils import (
    open_results_from_json,
    remove_duplicates,
    write_results_to_json,
)


def make_results_caracterization(scraper: str) -> Dict[str, int]:
    results = open_results_from_json(f"./results/{scraper}.json")

    return {
        "Distinct Time Complexities": len(
            {algorithm["time_complexity"] for algorithm in results}
        ),
        "Distinct Space Complexities": len(
            {algorithm["space_complexity"] for algorithm in results}
        ),
        "Non Trusted Time Complexities": sum(
            [1 for algorithm in results if not algorithm["trustable_time_complexity"]]
        ),
        "Non Trusted Space Complexities": sum(
            [1 for algorithm in results if not algorithm["trustable_space_complexity"]]
        ),
    }


def make_completition_rate(scraper: str) -> Dict[str, int]:
    results = open_results_from_json(f"./results/{scraper}.json")

    total = len(results)
    time_complexity, space_complexity = sum(
        1 for algorithm in results if not algorithm["time_complexity"]
    ), sum(1 for algorithm in results if not algorithm["space_complexity"])
    urls_with_problem = remove_duplicates(
        [
            algorithm["url"]
            for algorithm in results
            if not algorithm["time_complexity"] or not algorithm["space_complexity"]
        ]
    )

    return {
        "Total Algorithms": total,
        "Time Complexity Extracted": f"{total - time_complexity} extracted - {100 - (time_complexity / total) * 100}%",
        "Space Complexity Extracted": f"{total - space_complexity} extracted - {100 - (space_complexity / total) * 100}%",
        "URLs with problem": urls_with_problem,
    }


def calculate_metrics(
    true_positive: int, false_positive: int, true_negative: int, false_negative: int
) -> Dict[str, float]:
    accuracy = (true_positive + true_negative) / (
        true_positive + true_negative + false_positive + false_negative
    )
    precision = true_positive / (true_positive + false_positive)
    recall = true_positive / (true_positive + false_negative)
    f1_score = (2 * precision * recall) / (precision + recall)

    return {
        "True Positive": true_positive,
        "False Positive": false_positive,
        "True Negative": true_negative,
        "False negative": false_negative,
        "Accuracy": accuracy,
        "Precision": precision,
        "Recall": recall,
        "F1 Score": f1_score,
    }


def plot_confusion(
    title: str,
    true_positive: int,
    false_negative: int,
    false_positive: int,
    true_negative: int,
):
    array = numpy.array(
        [[true_positive, false_negative], [false_positive, true_negative]]
    )

    fig, ax = plot_confusion_matrix(conf_mat=array)
    plt.title("Space Complexity Confusion Matrix")
    plt.show()


def make_confusion_matrix(scraper: str) -> Dict[str, Dict[str, Any]]:
    manual_results = open_results_from_json(f"./results/manual_{scraper}.json")
    results = open_results_from_json(f"./results/{scraper}.json")

    time_metrics = {
        "true_positive": 0,
        "false_positive": 0,
        "true_negative": 0,
        "false_negative": 0,
    }

    space_metrics = {
        "true_positive": 0,
        "false_positive": 0,
        "true_negative": 0,
        "false_negative": 0,
    }

    for result, manual_result in zip(results, manual_results):
        # Time complexity
        if time_complexity := result["time_complexity"]:
            if time_complexity == manual_result["time_complexity"]:
                time_metrics["true_positive"] += 1
            else:
                time_metrics["false_positive"] += 1
        else:
            if not manual_result["time_complexity"]:
                time_metrics["true_negative"] += 1
            else:
                time_metrics["false_negative"] += 1

        # Space complexity
        if space_complexity := result["space_complexity"]:
            if space_complexity == manual_result["space_complexity"]:
                space_metrics["true_positive"] += 1
            else:
                space_metrics["false_positive"] += 1
        else:
            if not manual_result["space_complexity"]:
                space_metrics["true_negative"] += 1
            else:
                space_metrics["false_negative"] += 1

    # Calculating metrics
    time_complexity_metrics = calculate_metrics(**time_metrics)
    space_complexity_metrics = calculate_metrics(**space_metrics)

    # Plotting the confusion matrices
    plot_confusion("Time Complexity Confusion Matrix", **time_metrics)
    plot_confusion("Space Complexity Confusion Matrix", **space_metrics)

    # Return result
    return {
        "Time Complexity": time_complexity_metrics,
        "Space Complexity": space_complexity_metrics,
    }


def make_manual_results_boilerplate(scraper: str) -> None:
    results = open_results_from_json(f"./results/{scraper}.json")

    manual_results = [
        {"url": alg["url"], "time_complexity": " ", "space_complexity": " "}
        for alg in results
    ]

    write_results_to_json(f"./results/manual_{scraper}", manual_results)


def make_complexitys_classification(scraper: str) -> Dict[str, Dict[str, int]]:
    results = open_results_from_json(f"./results/{scraper}.json")

    time_classification = classify_complexity(
        [result["time_complexity"] for result in results]
    )
    space_classification = classify_complexity(
        [result["space_complexity"] for result in results]
    )

    return {
        "Time Complexity Classification": time_classification,
        "Space Complexity Classification": space_classification,
    }


def classify_complexity(complexities: List[str]) -> Dict[str, int]:
    constant, linear, exponential, polynomial, factorial, logarithmic = 0, 0, 0, 0, 0, 0
    for complexity in complexities:
        if complexity:
            if re.match(r"O\(1\)", complexity):
                constant += 1
            elif re.match(r"O\(\w\)", complexity):
                linear += 1
            elif re.match(r"O\(.*!.*\)", complexity):
                factorial += 1
            elif re.match(r"O\(.*log.*\)", complexity):
                logarithmic += 1
            elif re.match(r"O\(\d\^?\w\)", complexity):
                exponential += 1
            elif re.match(r"O\(\w\s*[\^\*\+]?\s*[\d\w\s]+.*\)", complexity) or re.match(
                r"O\(\d+\(\w\*\w\)", complexity
            ):
                polynomial += 1

    return {
        "Constant complexity": constant,
        "Linear complexity": linear,
        "Exponential complexity": exponential,
        "Polynomial complexity": polynomial,
        "Factorial complexity": factorial,
        "Log complexity": logarithmic,
    }


def make_algorithms_histogram(scraper: str):
    results = open_results_from_json(f"./results/{scraper}.json")

    count = Counter([result["url"] for result in results]).values()
    plt.hist(count)
    plt.xlabel("Número de Algoritmos")
    plt.ylabel("Frequência")
    plt.title("Histograma da Distribuição de Algoritmos")
    plt.show()


def traverse_tree(
    node: Union[Tag, NavigableString], depth: int, depths: Dict[str, List[int]]
) -> None:
    """
    Traverse the BeautifulSoup tree and populate the depths dictionary with tag names and their depths.

    Args:
        node: The current BeautifulSoup node.
        depth: Current depth of traversal.
        depths: Dictionary to populate with depths.
    """
    if isinstance(node, Tag):  # Using isinstance to check if node is a Tag type
        if node.name not in depths:
            depths[node.name] = []
        depths[node.name].append(depth)

        for child in node.children:
            traverse_tree(child, depth + 1, depths)


def calculate_html_nodes_depth(scraper: str) -> None:
    results = open_results_from_json(f"./results/{scraper}.json")
    urls = list(set(result["url"] for result in results))

    all_max_depths: List[int] = []
    all_num_nodes: List[int] = []

    for url in urls:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")

        depths: Dict[str, List[int]] = {}
        traverse_tree(soup, 0, depths)

        max_depth = max(max(depths[tag]) for tag in depths)
        num_nodes = sum(len(depths[tag]) for tag in depths)

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
    calculate_html_nodes_depth(scraper)
    make_algorithms_histogram(scraper)
