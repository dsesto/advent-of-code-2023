"""
--- Day 9: Mirage Maintenance ---
The OASIS produces a report of many values and how they are changing over time (your puzzle input). Each line in the
report contains the history of a single value.
To best protect the oasis, your environmental report should include a prediction of the next value in each history.
Analyze your OASIS report and extrapolate the next value for each history. What is the sum of these extrapolated values?

*ANSWER: 1921197370*

--- Part Two ---
Analyze your OASIS report again, this time extrapolating the previous value for each history. What is the sum of these
extrapolated values?

*ANSWER: 1124*
"""
import argparse
from typing import List


def main(input_file: str, part: int):
    all_series = read_series(input_file)
    extrapolate_forward = (part == 1)

    for series in all_series:
        add_next_series_element(series, forward=extrapolate_forward)

    element_to_check = -1 if extrapolate_forward else 0
    new_series_elements = [series[element_to_check] for series in all_series]
    new_series_elements_sum = sum(new_series_elements)
    print(f"Found new elements for series: {new_series_elements}. "
          f"Their sum is {new_series_elements_sum}.")
    return new_series_elements_sum


def read_series(file_path: str) -> List[List[int]]:
    with open(file_path, "r") as f:
        all_series = [list(map(int, line.rstrip().split())) for line in f]

    return all_series


def add_next_series_element(series: List[int], forward: bool):
    """Recursively decompose series to find the next element"""
    series_difference = []
    for i in range(len(series)):
        if i == 0:
            continue

        series_difference.append(series[i] - series[i - 1])

    if all([x == 0 for x in series_difference]):
        if forward:
            return series[-1]
        else:
            return series[0]
    else:
        current_series_diff = add_next_series_element(series_difference, forward)
        if forward:
            series.append(series[-1] + current_series_diff)
            return series[-1]
        else:
            series.insert(0, series[0] - current_series_diff)
            return series[0]


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input-file", required=True)
    parser.add_argument("-p", "--part", type=int, choices=[1, 2], required=True)
    args = parser.parse_args()

    main(args.input_file, args.part)
