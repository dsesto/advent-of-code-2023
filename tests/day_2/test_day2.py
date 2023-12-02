import os.path

from advent_calendar.day_2 import day2


def test_day2_should_return_sum_of_possible_game_ids():
    input_file = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "resources",
        "input_part1.txt",
    )

    assert (1 + 2 + 5) == day2.main(input_file, (12, 13, 14), 1)


def test_day2_should_work_with_my_own_example():
    # The file tested here adds a couple of corner cases, to check the "<=" use
    input_file = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "resources",
        "input_part1_custom.txt",
    )

    assert (1 + 2 + 5 + 6) == day2.main(input_file, (12, 13, 14), 1)


def test_day2_should_return_sum_of_powers_of_minimum_sets_in_part2():
    input_file = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "resources",
        "input_part1.txt",
    )

    assert 2286 == day2.main(input_file, None, 2)
