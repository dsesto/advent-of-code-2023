"""
--- Day 6: Wait For It ---
As part of signing up [for a boat competition], you get a sheet of paper (your puzzle input) that lists the time allowed
for each race and also the best distance ever recorded in that race. To guarantee you win the grand prize, you need to
make sure you go farther in each race than the current record holder.
Each [boat] has a big button on top. Holding down the button charges the boat, and releasing the button allows the boat
to move. Boats move faster if their button was held longer, but time spent holding the button counts against the total
race time. You can only hold the button at the start of the race, and boats don't move until the button is released.
Your toy boat has a starting speed of zero millimeters per millisecond. For each whole millisecond you spend at the
beginning of the race holding down the button, the boat's speed increases by one millimeter per millisecond.
To see how much margin of error you have, determine the number of ways you can beat the record in each race.
Determine the number of ways you could beat the record in each race. What do you get if you multiply these numbers together?

*ANSWER: 505494*

--- Part Two ---
There's really only one race - ignore the spaces between the numbers on each line.
How many ways can you beat the record in this one much longer race?

*ANSWER: 23632299*
"""
import argparse
from dataclasses import dataclass
from typing import List

import numpy as np


@dataclass
class Race:
    time: int
    record: int

    def get_distance_combinations(self):
        return [t * (self.time - t) for t in range(self.time)]

    def get_winning_strategies(self):
        return [d for d in self.get_distance_combinations() if d > self.record]


def main(input_file: str, part: int):
    races = read_races(input_file, part)
    winning_strategies = [len(r.get_winning_strategies()) for r in races]
    winning_strategies_mult = np.prod(winning_strategies)
    print(f"Found the following amount of winning strategies: {winning_strategies}. "
          f"Their product is {winning_strategies_mult}.")
    return winning_strategies_mult


def read_races(file_path: str, part: int) -> List[Race]:
    races = []

    with open(file_path, "r") as f:
        line_id = 0
        times = []
        records = []
        for line in f:
            line = line.rstrip()
            if part == 1:
                if line_id == 0:
                    times = [int(t) for t in line.replace("Time:", "").split()]
                else:
                    records = [int(r) for r in line.replace("Distance:", "").split()]
            elif part == 2:
                if line_id == 0:
                    times = [int("".join(line.replace("Time:", "").split()))]
                else:
                    records = [int("".join(line.replace("Distance:", "").split()))]
            line_id += 1

        for time, record in zip(times, records):
            races.append(Race(time, record))

    return races


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input-file", required=True)
    parser.add_argument("-p", "--part", type=int, choices=[1, 2], required=True)
    args = parser.parse_args()

    main(args.input_file, args.part)
