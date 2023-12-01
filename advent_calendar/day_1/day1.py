"""
--- Day 1: Trebuchet?! ---
[...]
The newly-improved calibration document consists of lines of text; each line originally contained
a specific calibration value that the Elves now need to recover. On each line, the calibration value
can be found by combining the first digit and the last digit (in that order) to form a single
two-digit number.
Consider your entire calibration document. What is the sum of all of the calibration values?

*ANSWER: 55208*

--- Part Two ---
Your calculation isn't quite right. It looks like some of the digits are actually spelled out with
letters: one, two, three, four, five, six, seven, eight, and nine also count as valid "digits".
Equipped with this new information, you now need to find the real first and last digit on each line.
What is the sum of all of the calibration values?

*ANSWER: 54578*
"""
import argparse
from typing import List


def main(input_file: str, part: int):
    words = read_words(input_file)

    if part == 1:
        return find_calibration_value_numbers(words)

    return find_calibration_value_numbers_and_words(words)


def find_calibration_value_numbers(words: List[str]):
    """
    Find the first and last number (in digit form) on each word, combine them into a single
    number, and sum them all together.
    """
    calibration_value = 0
    for word in words:
        first_number = [c for c in word if c.isnumeric()][0]
        last_number = [c for c in word if c.isnumeric()][-1]
        calibration_value += int(first_number + last_number)

    print(f"The calibration value of these {len(words)} words is: {calibration_value}")
    return calibration_value


def find_calibration_value_numbers_and_words(words: List[str]):
    number_words = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]

    new_words = []
    for word in words:
        found_number_words = [word.find(w) for w in number_words]
        while max(found_number_words) >= 0:
            # Keep looking for substrings until none is found
            first_found_number_word_num = found_number_words.index(min([f for f in found_number_words if f >= 0])) + 1
            # To cover for the case "eighthree" = "83", where letter "T" is used twice, a possible
            # solution is to keep the first and last letter during the replacement; e.g. "eight" = "e8t".
            # This works on the assumption that only 1 letter can overlap between number words.
            first_found_number_word_w = number_words[first_found_number_word_num - 1]
            word = word.replace(
                first_found_number_word_w,
                f"{first_found_number_word_w[0]}{str(first_found_number_word_num)}{first_found_number_word_w[-1]}",
            )
            found_number_words = [word.find(w) for w in number_words]
        new_words.append(word)

    return find_calibration_value_numbers(new_words)


def read_words(file_path: str) -> List[str]:
    with open(file_path, "r") as f:
        words = [line.rstrip() for line in f]

    return words


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input-file", required=True)
    parser.add_argument("-p", "--part", type=int, choices=[1, 2], required=True)
    args = parser.parse_args()

    main(args.input_file, args.part)
