import os

import pytest

from advent_calendar.day_11 import day11


def test_expand_universe():
    input_file = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "resources",
        "input.txt",
    )
    expanded_input_file = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "resources",
        "expanded_input.txt",
    )
    expected_expanded_sky = day11.read_sky(expanded_input_file)

    sky = day11.read_sky(input_file)
    expanded_sky = day11.expand_universe(sky)

    assert expected_expanded_sky == expanded_sky


def test_expand_universe_mathematically():
    input_file = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "resources",
        "input.txt",
    )
    expected_expanded_sky = [
        [(1, 1), (1, 1), (3, 1), "#", (1, 1), (3, 1), (1, 1), (1, 1), (3, 1), (1, 1)],
        [(1, 1), (1, 1), (3, 1), (1, 1), (1, 1), (3, 1), (1, 1), "#", (3, 1), (1, 1)],
        ["#", (1, 1), (3, 1), (1, 1), (1, 1), (3, 1), (1, 1), (1, 1), (3, 1), (1, 1)],
        [(1, 3), (1, 3), (3, 3), (1, 3), (1, 3), (3, 3), (1, 3), (1, 3), (3, 3), (1, 3)],
        [(1, 1), (1, 1), (3, 1), (1, 1), (1, 1), (3, 1), "#", (1, 1), (3, 1), (1, 1)],
        [(1, 1), "#", (3, 1), (1, 1), (1, 1), (3, 1), (1, 1), (1, 1), (3, 1), (1, 1)],
        [(1, 1), (1, 1), (3, 1), (1, 1), (1, 1), (3, 1), (1, 1), (1, 1), (3, 1), "#"],
        [(1, 3), (1, 3), (3, 3), (1, 3), (1, 3), (3, 3), (1, 3), (1, 3), (3, 3), (1, 3)],
        [(1, 1), (1, 1), (3, 1), (1, 1), (1, 1), (3, 1), (1, 1), "#", (3, 1), (1, 1)],
        ["#", (1, 1), (3, 1), (1, 1), "#", (3, 1), (1, 1), (1, 1), (3, 1), (1, 1)],
    ]

    sky = day11.read_sky(input_file)
    expanded_sky = day11.expand_universe_mathematically(sky, expansion=3)

    assert expected_expanded_sky == expanded_sky


def test_transpose_matrix():
    matrix = [
        ["a", "b", "c"],
        ["d", "e", "f"],
    ]
    expected_output = [
        ["a", "d"],
        ["b", "e"],
        ["c", "f"],
    ]

    output = day11.transpose_matrix(matrix)

    assert output == expected_output


def test_find_distances_between_galaxies_mathematically():
    expanded_sky = [
        [(1, 1), (1, 1), (3, 1), "#"],
        [(1, 1), (1, 1), (3, 1), (1, 1)],
        ["#", (1, 1), (3, 1), (1, 1)],
        [(1, 3), (1, 3), (3, 3), (1, 3)],
        [(1, 1), (1, 1), (3, 1), (1, 1)],
        [(1, 1), "#", (3, 1), (1, 1)],
    ]
    galaxies = day11.find_galaxies(expanded_sky)

    distances = day11.find_distances_between_galaxies_mathematically(expanded_sky, galaxies)

    assert distances == [
        [5 + 2, 4 + 7],
        [5 + 2, 1 + 5],
        [4 + 7, 1 + 5],
    ]


def test_find_distances_between_galaxies_mathematically_extra():
    expanded_sky = [
        ["#", (1, 1), (3, 1), (1, 1)],
        [(1, 1), (1, 1), (3, 1), (1, 1)],
        ["#", (1, 1), (3, 1), "#"],
    ]
    galaxies = day11.find_galaxies(expanded_sky)

    distances = day11.find_distances_between_galaxies_mathematically(expanded_sky, galaxies)

    assert distances == [
        [0 + 2, 5 + 2],
        [0 + 2, 5 + 0],
        [5 + 2, 5 + 0],
    ]


def test_part_1():
    input_file = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "resources",
        "input.txt",
    )
    res = day11.main(input_file, part=1)

    assert res == 374


@pytest.mark.parametrize("expansion,result", [(10, 1030), (100, 8410)])
def test_part_2(expansion, result):
    input_file = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "resources",
        "input.txt",
    )
    res = day11.main(input_file, part=2, expansion=expansion)

    assert res == result
