"""
--- Day 3: Gear Ratios ---
The engine schematic (your puzzle input) consists of a visual representation of the engine. There are lots of numbers
and symbols you don't really understand, but apparently any number adjacent to a symbol, even diagonally, is a "part
number" and should be included in your sum. (Periods (.) do not count as a symbol.)
What is the sum of all of the part numbers in the engine schematic?

*ANSWER: 557705*

--- Part Two ---
The missing part wasn't the only issue - one of the gears in the engine is wrong. A gear is any * symbol that is
adjacent to exactly two part numbers. Its gear ratio is the result of multiplying those two numbers together.
What is the sum of all of the gear ratios in your engine schematic?

*ANSWER: 84266818*
"""
import argparse
from typing import List, Tuple, Dict

import numpy as np


def main(input_file: str, part: int):
    schematic = read_schematic(input_file)

    if part == 1:
        adjacent_numbers = get_numbers_adjacent_to_symbol(schematic)
        adjacent_numbers_sum = sum(adjacent_numbers)
        print(f"Found {len(adjacent_numbers)} numbers adjacent to a symbol: {adjacent_numbers}. "
              f"Their sum is {adjacent_numbers_sum}")
        return adjacent_numbers_sum
    else:
        gears = get_numbers_adjacent_to_gear(schematic)
        gear_ratios = [np.prod(numbers) for numbers in gears.values()]
        gear_ratios_sum = sum(gear_ratios)
        print(f"Found {len(gears)} gears: {gears}. "
              f"The sum of all their gear ratios is: {gear_ratios_sum}")
        return gear_ratios_sum


def get_numbers_adjacent_to_symbol(schematic: List[str]):
    """
    Finds all numbers that are adjacent to a symbol.
    """
    adjacent_numbers = []
    all_numbers = get_all_numbers(schematic)

    min_row, max_row, min_col, max_col = 0, len(schematic) - 1, 0, len(schematic[0]) - 1
    for number, number_pos in all_numbers:
        row_idx = number_pos[0]
        col_idx = number_pos[1]
        positions_to_check = []

        num_rows_to_check = 3  # Previous, current, next
        num_cols_to_check = len(str(number)) + 2  # Previous + N current + next
        for r in range(num_rows_to_check):
            for c in range(num_cols_to_check):
                positions_to_check.append(
                    (
                        min(max(row_idx - 1 + r, min_row), max_row),
                        min(max(col_idx - 1 + c, min_col), max_col),
                    )
                )
        positions_to_check = list(set(positions_to_check))

        for pos in positions_to_check:
            character = schematic[pos[0]][pos[1]]
            if not character.isalnum() and character != ".":
                adjacent_numbers.append(number)
                break

    return sorted(adjacent_numbers)


def get_all_numbers(schematic: List[str]) -> List[Tuple[int, Tuple[int, int]]]:
    """
    Returns a list of all the numbers in the schematic, along with their position. E.g.:
    (142, (3, 1)) -> Number 142 can be found in row 3, column 1
    """
    numbers = []
    for row_idx, row in enumerate(schematic):
        row = "".join([c if c.isnumeric() else "." for c in row])
        row = row.split(".")

        col_idx = 0
        for element in row:
            if element.isnumeric():
                numbers.append((int(element), (row_idx, col_idx)))
                col_idx += len(element) + 1
            else:
                # After splitting by ".", if there's a non-numeric character, it means that there
                # were 2 consecutive "."
                col_idx += 1

    return numbers


def get_numbers_adjacent_to_gear(schematic: List[str]) -> Dict[Tuple[int, int], List[int]]:
    gears_found = {}  # Keys are the position of a gear; values are the list of numbers touching the gear
    all_numbers = get_all_numbers(schematic)

    min_row, max_row, min_col, max_col = 0, len(schematic) - 1, 0, len(schematic[0]) - 1
    for number, number_pos in all_numbers:
        row_idx = number_pos[0]
        col_idx = number_pos[1]
        positions_to_check = []

        num_rows_to_check = 3  # Previous, current, next
        num_cols_to_check = len(str(number)) + 2  # Previous + N current + next
        for r in range(num_rows_to_check):
            for c in range(num_cols_to_check):
                positions_to_check.append(
                    (
                        min(max(row_idx - 1 + r, min_row), max_row),
                        min(max(col_idx - 1 + c, min_col), max_col),
                    )
                )
        positions_to_check = list(set(positions_to_check))

        for pos in positions_to_check:
            character = schematic[pos[0]][pos[1]]
            character_position = (pos[0], pos[1])
            if character == "*":
                if character_position not in gears_found:
                    gears_found[character_position] = []
                gears_found[character_position].append(number)

    # Gears are gears only if they are adjacent to exactly 2 numbers
    gears_found = {k: v for k, v in gears_found.items() if len(v) == 2}
    return gears_found


def read_schematic(file_path: str) -> List[str]:
    with open(file_path, "r") as f:
        schematic = [line.rstrip() for line in f]

    return schematic


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input-file", required=True)
    parser.add_argument("-p", "--part", type=int, choices=[1, 2], required=True)
    args = parser.parse_args()

    main(args.input_file, args.part)
