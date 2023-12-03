import os

from advent_calendar.day_3 import day3


def test_get_all_numbers_should_return_all_numbers():
    input_file = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "resources",
        "input.txt",
    )
    schematic = day3.read_schematic(input_file)
    numbers = day3.get_all_numbers(schematic)

    assert numbers == [
        (467, (0, 0)),
        (114, (0, 5)),
        (35, (2, 2)),
        (633, (2, 6)),
        (617, (4, 0)),
        (58, (5, 7)),
        (592, (6, 2)),
        (755, (7, 6)),
        (664, (9, 1)),
        (598, (9, 5)),
    ]


def test_get_numbers_adjacent_to_symbol_should_return_expected_numbers():
    input_file = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "resources",
        "input.txt",
    )
    schematic = day3.read_schematic(input_file)
    numbers = day3.get_numbers_adjacent_to_symbol(schematic)

    assert numbers == sorted([467, 35, 633, 617, 592, 755, 664, 598])


def test_get_numbers_adjacent_to_gear_should_return_all_gears():
    schematic = [
        ".1....2.3..6*",
        "..*4..5*.....",
    ]
    gears = day3.get_numbers_adjacent_to_gear(schematic)

    assert gears == {
        (1, 2): [1, 4],
    }
