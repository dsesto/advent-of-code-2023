import os

from advent_calendar.day_8 import day8


def test_part_1_should_work_with_straightforward_paths():
    input_file = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "resources",
        "input1.txt",
    )

    result = day8.main(input_file, part=1)

    assert result == 2


def test_part_1_should_work_with_repeated_paths():
    input_file = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "resources",
        "input2.txt",
    )

    result = day8.main(input_file, part=1)

    assert result == 6


def test_part_2_should_return_lcm_of_all_paths():
    input_file = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "resources",
        "input3.txt",
    )

    result = day8.main(input_file, part=2)

    assert result == 6
