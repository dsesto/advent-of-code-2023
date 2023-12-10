import os

from advent_calendar.day_9 import day9


def test_part_1_should_return_the_sum_of_all_forward_extrapolated_elements():
    input_file = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "resources",
        "input.txt",
    )

    result = day9.main(input_file, part=1)

    assert result == 114


def test_part_1_should_return_the_sum_of_all_backward_extrapolated_elements():
    input_file = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "resources",
        "input.txt",
    )

    result = day9.main(input_file, part=2)

    assert result == 2
