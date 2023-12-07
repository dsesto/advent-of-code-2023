import os

from advent_calendar.day_7 import day7


def test_read_hands_should_return_hands_computed_for_part_1():
    input_file = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "resources",
        "input.txt",
    )

    hands = day7.read_hands(input_file, part=1)

    assert len(hands) == 5
    assert hands[0].cards == ["3", "2", "T", "3", "K"]
    assert hands[0].bid == 765
    assert hands[0].type == 1
    assert hands[0].cards_strengths == [1, 0, 8, 1, 11]
    assert hands[1].type == 3
    assert hands[1].cards_strengths == [8, 3, 3, 9, 3]
    assert hands[2].type == 2
    assert hands[3].type == 2
    assert hands[4].type == 3


def test_read_hands_should_return_hands_computed_for_part_2():
    input_file = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "resources",
        "input.txt",
    )

    hands = day7.read_hands(input_file, part=2)

    assert len(hands) == 5
    assert hands[0].cards == ["3", "2", "T", "3", "K"]
    assert hands[0].bid == 765
    assert hands[0].type == 1
    assert hands[0].cards_strengths == [2, 1, 9, 2, 11]
    assert hands[1].type == 5
    assert hands[1].cards_strengths == [9, 4, 4, 0, 4]
    assert hands[2].type == 2
    assert hands[3].type == 5
    assert hands[4].type == 5


def test_part_1_should_return_total_winnings():
    input_file = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "resources",
        "input.txt",
    )

    result = day7.main(input_file, part=1)

    assert result == 6440


def test_part_2_should_return_total_winnings():
    input_file = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "resources",
        "input.txt",
    )

    result = day7.main(input_file, part=2)

    assert result == 5905
