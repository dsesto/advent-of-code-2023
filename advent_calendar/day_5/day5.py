"""
--- Day 5: If You Give A Seed A Fertilizer ---
The almanac (your puzzle input) lists all of the seeds that need to be planted. It also lists what type of soil to use
with each kind of seed, what type of fertilizer to use with each kind of soil, etc. The last mapping points to the
location where the seed can grow. The maps describe entire ranges of numbers that can be converted. Any source numbers
that aren't mapped correspond to the same destination number.
What is the lowest location number that corresponds to any of the initial seed numbers?

*ANSWER: 251346198*

--- Part Two ---
The seeds: line actually describes ranges of seed numbers.
Within each pair, the first value is the start of the range and the second value is the length of the range.
What is the lowest location number that corresponds to any of the initial seed numbers?

*ANSWER: 72263011*
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass
from typing import List, Optional


@dataclass
class Interval:
    """
    An interval illustrates a range of input IDs (src) with their corresponding mapping in the output (dst).
    For part 2 of the challenge we will also define ranges that are not a mapping, thus why the dst is optional.
    """
    src_start: int
    dst_start: Optional[int]
    length: int

    def belongs_to_interval(self, value: int):
        return self.min <= value <= self.max

    def map(self, value: int):
        return self.dst_start + (value - self.src_start)

    @property
    def min(self):
        """Included in the interval"""
        return self.src_start

    @property
    def max(self):
        """Included in the interval"""
        return self.src_start + self.length - 1

    def compute_overlap(self, *intervals: Interval) -> List[Interval]:
        """
        Computes the overlap of the current interval with a list of intervals, which represents a complete mapping.
        The output overlapping points are in dst units.
        """

        def create_dst_interval(inter: Interval, src_min: int, src_max: int):
            return Interval(inter.map(src_min), None, src_max - src_min + 1)

        overlaps = []
        for interval in intervals:
            if interval.min <= self.min <= interval.max and interval.min <= self.max <= interval.max:
                # Case 1: seed interval completely inside mapping interval
                overlaps.append(create_dst_interval(interval, self.min, self.max))
            elif interval.min <= self.min <= interval.max < self.max:
                # Case 2: seed interval starts inside mapping interval but continues in next mapping interval
                overlaps.append(create_dst_interval(interval, self.min, interval.max))
            elif self.min < interval.min <= self.max <= interval.max:
                # Case 3: seed interval starts in previous interval and ends inside current mapping interval
                overlaps.append(create_dst_interval(interval, interval.min, self.max))
            elif self.min < interval.min and interval.max < self.max:
                # Case 4: mapping interval completely inside seed interval
                overlaps.append(create_dst_interval(interval, interval.min, interval.max))

        return overlaps


def main(input_file: str, part: int):
    almanac = read_almanac(input_file, part)

    if part == 1:
        seed_locations = find_seed_locations(*almanac)
        min_seed_location = min(seed_locations)
        print(f"Found seed locations {seed_locations}. The closest one is {min_seed_location}.")
        return min_seed_location
    else:
        seeds, mappings = almanac[0], almanac[1:]
        mappings = fill_mappings(*mappings)
        final_seed_locations = []
        find_closest_seed_location(seeds, final_seed_locations, *mappings)
        closest_location = min([i.min for i in final_seed_locations])
        print(f"Found {len(final_seed_locations)} final locations. "
              f"The closest one is: {closest_location}")
        return closest_location


def read_almanac(file_path: str, part: int):
    seeds = []
    seed_to_soil = []
    soil_to_fertilizer = []
    fertilizer_to_water = []
    water_to_light = []
    light_to_temperature = []
    temperature_to_humidity = []
    humidity_to_location = []

    def parse_map(mappings: List[Interval], row: str):
        dst_start, src_start, length = [int(x) for x in row.split(" ")]
        mappings.append(Interval(src_start, dst_start, length))

    with open(file_path, "r") as f:
        current_map = None
        for line in f:
            line = line.rstrip()
            if line == "":
                continue
            elif line.startswith("seeds: "):
                seeds = [int(x) for x in line.split("seeds: ", 1)[1].split(" ")]
                if part == 2:
                    seed_intervals = []
                    i = 0
                    while i < len(seeds):
                        seed_intervals.append(Interval(seeds[i], None, seeds[i + 1]))
                        i += 2
                    seeds = seed_intervals
                continue
            elif line == "seed-to-soil map:":
                current_map = seed_to_soil
            elif line == "soil-to-fertilizer map:":
                current_map = soil_to_fertilizer
            elif line == "fertilizer-to-water map:":
                current_map = fertilizer_to_water
            elif line == "water-to-light map:":
                current_map = water_to_light
            elif line == "light-to-temperature map:":
                current_map = light_to_temperature
            elif line == "temperature-to-humidity map:":
                current_map = temperature_to_humidity
            elif line == "humidity-to-location map:":
                current_map = humidity_to_location

            if line.endswith(" map:"):
                continue

            parse_map(current_map, line)

    return seeds, seed_to_soil, soil_to_fertilizer, fertilizer_to_water, water_to_light, light_to_temperature, temperature_to_humidity, humidity_to_location


def find_seed_locations(seeds: List[int], *mappings: List[Interval]):
    """Finds locations of seeds the naive way, iterating their map completely."""
    locations = []
    for seed in seeds:
        current_element = seed
        for mapping in mappings:
            mapping_found = False
            for interval in mapping:
                if interval.belongs_to_interval(current_element):
                    current_element = interval.map(current_element)
                    mapping_found = True
                if mapping_found:
                    break
        locations.append(current_element)

    return locations


def fill_mappings(*mappings: List[Interval]):
    """
    To ease computations, fill the gaps between explicit intervals with 1-to-1 mappings.
    """

    def create_implicit_interval(start: int, end: int):
        """Start is included, end is excluded"""
        return Interval(start, start, end - start)

    new_mappings = []
    for mapping in mappings:
        new_intervals = sorted([i for i in mapping], key=lambda i: i.min)
        if new_intervals[0].min != 0:
            new_intervals.insert(0, create_implicit_interval(0, new_intervals[0].min))
        new_intervals.append(create_implicit_interval(new_intervals[-1].max + 1, 100_000_000_000))

        i = 0
        while i < len(new_intervals) - 1:
            if new_intervals[i].max + 1 < new_intervals[i + 1].min:
                new_intervals.insert(i + 1,
                                     create_implicit_interval(new_intervals[i].max + 1, new_intervals[i + 1].min))
            i += 1

        new_mappings.append(new_intervals)

    return new_mappings


def find_closest_seed_location(seeds: List[Interval],
                               final_seed_locations: List[Interval],
                               *mappings: List[Interval]):
    """
    Recursively iterates over all "sources", starting with seeds, and following with the corresponding dst mapping
    of each iteration. During the recursion, it populates a list of final locations that is only updated when the last
    mapping level (i.e. humidity-to-location) is reached.
    """
    for seed_interval in seeds:
        overlaps = seed_interval.compute_overlap(*mappings[0])

        if len(mappings) == 1:
            final_seed_locations.extend(overlaps)
        if len(mappings) > 1:
            find_closest_seed_location(overlaps, final_seed_locations, *mappings[1:])


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input-file", required=True)
    parser.add_argument("-p", "--part", type=int, choices=[1, 2], required=True)
    args = parser.parse_args()

    main(args.input_file, args.part)
