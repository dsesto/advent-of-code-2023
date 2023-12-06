import os

from advent_calendar.day_6 import day6


def test_read_races_should_return_races_in_file_in_part1_format():
    input_file = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "resources",
        "input.txt",
    )

    races = day6.read_races(input_file, part=1)

    assert len(races) == 3
    assert races[0].time == 7
    assert races[0].record == 9
    assert races[1].time == 15
    assert races[1].record == 40
    assert races[2].time == 30
    assert races[2].record == 200


def test_read_races_should_return_races_in_file_in_part2_format():
    input_file = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "resources",
        "input.txt",
    )

    races = day6.read_races(input_file, part=2)

    assert len(races) == 1
    assert races[0].time == 71530
    assert races[0].record == 940200


def test_part1_should_return_product_of_winning_strategies():
    input_file = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "resources",
        "input.txt",
    )

    result = day6.main(input_file, part=1)

    assert result == 288
