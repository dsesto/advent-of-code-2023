import os

import pytest

from advent_calendar.day_10 import day10


@pytest.mark.parametrize(
    "input_file, max_distance",
    (("input1_easy.txt", 4), ("input1_difficult.txt", 4), ("input2_easy.txt", 8), ("input2_difficult.txt", 8),)
)
def test_part_1_should_return_the_max_distance_in_the_loop(input_file, max_distance):
    input_file = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "resources",
        input_file,
    )

    result = day10.main(input_file, part=1)

    assert result == max_distance


@pytest.mark.parametrize(
    "input_file, i_area",
    (("input3.txt", 8), ("input4.txt", 10),)
)
def test_part_2_should_return_the_count_of_inside_areas(input_file, i_area):
    input_file = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "resources",
        input_file,
    )

    result = day10.main(input_file, part=2)

    assert result == i_area
