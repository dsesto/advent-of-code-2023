import os

from advent_calendar.day_5 import day5
from advent_calendar.day_5.day5 import Interval


def test_find_seed_locations():
    input_file = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "resources",
        "input.txt",
    )

    almanac = day5.read_almanac(input_file, part=1)
    locations = day5.find_seed_locations(*almanac)

    assert locations == [82, 43, 86, 35]


def test_part2():
    input_file = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "resources",
        "input.txt",
    )

    location = day5.main(input_file, part=2)

    assert location == 46


def test_compute_overlap():
    seeds = Interval(5, None, 10)

    mapping1 = [
        Interval(1, 1000, 3),
        Interval(3, 2000, 5),
        Interval(10, 3000, 2),
        Interval(12, 4000, 8),
        Interval(20, 5000, 10),
    ]
    mappings = [mapping1]
    mappings = day5.fill_mappings(*mappings)

    overlaps = seeds.compute_overlap(*mappings[0])

    # Expected overlap in src:
    # 5-7, (8-9), 10-11, 12-14
    # Expected overlap in dst:
    # 2002-2004, 8-9, 3000-3001, 4000-4002
    overlaps = sorted(overlaps, key=lambda x: x.min)
    assert len(mappings[0]) == 5 + 3  # 1 populated at the beginning, 1 in the middle, 1 at the end
    assert len(overlaps) == 4
    assert overlaps[0].min == 8
    assert overlaps[0].max == 9
    assert overlaps[1].min == 2002
    assert overlaps[1].max == 2004
    assert overlaps[2].min == 3000
    assert overlaps[2].max == 3001
    assert overlaps[3].min == 4000
    assert overlaps[3].max == 4002
