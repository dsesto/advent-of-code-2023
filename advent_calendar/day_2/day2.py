"""
--- Day 2: Cube Conundrum ---
An elf plays with us multiple iterations of a game, that plays as follows:
The elf fills a bag with a random amount of cubes, of colours red, green and blue. Then, the elf grabs a handful of
random cubes and shows them to us. This is repeated several times per game. We record each of them as follows:
    Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
This means that in game 1, we were shown 3 handful of cubes: the first one with 3 blue cubes and 4 red, the second one
with 1 red, 2 green and 6 blue; and the third one with only 2 green.
The elf would first like to know which games would have been possible if the bag contained only 12 red cubes, 13 green
cubes, and 14 blue cubes?
What is the sum of the IDs of those games?

*ANSWER: 2061*

--- Part Two ---
In each game you played, what is the fewest number of cubes of each color that could have been in the bag to make the
game possible?
The power of a set of cubes is equal to the numbers of red, green, and blue cubes multiplied together.
For each game, find the minimum set of cubes that must have been present. What is the sum of the power of these sets?

*ANSWER: 72596*
"""
import argparse
from dataclasses import dataclass
from typing import List, Tuple, Optional

import numpy as np


@dataclass
class Sample:
    red: int = 0
    green: int = 0
    blue: int = 0


@dataclass
class Game:
    id: int
    samples: List[Sample]

    def is_possible(self, red, green, blue):
        """
        Determines whether a game with a certain amount of R, G, and B pieces is possible,
        based on the samples shown.
        """
        return (all([s.red <= red for s in self.samples]) &
                all([s.green <= green for s in self.samples]) &
                all([s.blue <= blue for s in self.samples]))

    def find_minimum_set(self):
        """
        Find the minimum amount of cubes of each color needed to make a game possible
        """
        minimum_red = max([s.red for s in self.samples])
        minimum_green = max([s.green for s in self.samples])
        minimum_blue = max([s.blue for s in self.samples])

        return minimum_red, minimum_green, minimum_blue


def main(input_file: str, bag_content: Optional[Tuple[int, int, int]], part: int):
    games = read_input(input_file)

    if part == 1:
        return find_possible_games(games, bag_content)
    else:
        return find_minimum_sets(games)


def read_input(file_path: str) -> List[Game]:
    games = []
    with open(file_path, "r") as f:
        for line in f:
            line = line.rstrip()
            game_id, game_samples = line.split(": ", 1)

            # Find the game ID
            game_id = int(game_id.split(" ", 1)[1])

            # Find the samples of the game
            game_samples = game_samples.split("; ")
            samples = []
            for game_sample in game_samples:
                samples.append(_parse_sample(game_sample))

            games.append(Game(game_id, samples))

    return games


def find_possible_games(games: List[Game], bag_content: Tuple[int, int, int]):
    """
    Computes the sum of the IDs of all the games that are possible to play, given a certain amount of cubes.
    """
    if not bag_content:
        raise ValueError("You must define a bag content when solving part 1.")

    possible_games = [game for game in games if game.is_possible(*bag_content)]
    possible_games_ids = [g.id for g in possible_games]
    sum_possible_games_ids = sum(possible_games_ids)

    print(f"The possible games are {possible_games_ids}, which sum {sum_possible_games_ids}.")
    return sum_possible_games_ids


def find_minimum_sets(games: List[Game]):
    """
    Computes the sum of the power of all the sets that account for the minimum amount of necessary cubes to make
    each game possible.
    """
    minimum_sets = [np.prod(list(g.find_minimum_set())) for g in games]
    sum_minimum_sets = sum(minimum_sets)

    print(f"The minimum sets for each game are {minimum_sets}, which sum {sum_minimum_sets}.")
    return sum_minimum_sets


def _parse_sample(sample_text: str) -> Sample:
    samples = sample_text.split(", ")
    sample_red, sample_green, sample_blue = 0, 0, 0
    for sample in samples:
        sample_amount = int(sample.split(" ", 1)[0])
        if "red" in sample:
            sample_red = sample_amount
        elif "green" in sample:
            sample_green = sample_amount
        else:
            sample_blue = sample_amount
    return Sample(sample_red, sample_green, sample_blue)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input-file", required=True)
    parser.add_argument("-b", "--bag-content", type=int, nargs=3)
    parser.add_argument("-p", "--part", type=int, choices=[1, 2], required=True)
    args = parser.parse_args()

    main(args.input_file, args.bag_content, args.part)
