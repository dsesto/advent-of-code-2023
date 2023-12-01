import os.path

import pytest

from advent_calendar.day_1 import day1


def test_day1_should_return_calibration_value_for_part1():
    calibration_file = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "resources",
        "calibration_file_part1.txt",
    )

    assert 142 == day1.main(calibration_file, part=1)


def test_day1_should_return_calibration_value_for_part2():
    calibration_file = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "resources",
        "calibration_file_part2.txt",
    )

    assert 281 == day1.main(calibration_file, part=2)


@pytest.mark.parametrize(
    "word,output",
    [
        ("eightthree", 83),
        ("sevenine", 79),
        ("one4one56bnhf", 16),
    ]
)
def test_day1_should_return_calibration_value_for_part2_with_special_cases(word, output):
    """
    The problem definition is not clear about whether words like "eighthree" end up being
    translated as "8hree" or "83".
    This Reddit post states that the solution is the latter:
    https://www.reddit.com/r/adventofcode/comments/1884fpl/2023_day_1for_those_who_stuck_on_part_2/
    """
    words = [word]

    assert output == day1.find_calibration_value_numbers_and_words(words)
