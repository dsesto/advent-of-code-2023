import os

from advent_calendar.day_4 import day4


def test_get_cards_points_should_return_all_points():
    input_file = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "resources",
        "input.txt",
    )

    cards = day4.read_cards(input_file)
    points = day4.get_cards_points(cards)

    assert points == [8, 2, 2, 1, 0, 0]


def test_get_cards_counts():
    input_file = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "resources",
        "input.txt",
    )

    cards = day4.read_cards(input_file)
    points = day4.get_cards_counts(cards)

    assert points == [1, 2, 4, 8, 14, 1]
