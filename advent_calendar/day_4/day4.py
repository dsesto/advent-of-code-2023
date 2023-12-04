"""
--- Day 4: Scratchcards ---
Each scratchcard has two lists of numbers separated by a vertical bar (|): a list of winning numbers and then a list of
numbers you have. You organize the information into a table (your puzzle input).
You have to figure out which of the numbers you have appear in the list of winning numbers. The first match makes the
card worth one point and each match after the first doubles the point value of that card.
How many points are they worth in total?

*ANSWER: 23941*

--- Part Two ---
The rules have actually been printed on the back of every card this whole time [and you got them wrong].
Instead, scratchcards only cause you to win more scratchcards equal to the number of winning numbers you have.
Specifically, you win copies of the scratchcards below the winning card equal to the number of matches. So, if card 10
were to have 5 matching numbers, you would win one copy each of cards 11, 12, 13, 14, and 15.
Copies of scratchcards are scored like normal scratchcards and have the same card number as the card they copied.
Process all of the original and copied scratchcards until no more scratchcards are won. Including the original set of
scratchcards, how many total scratchcards do you end up with?

*ANSWER: 5571760*
"""
import argparse
import math
from dataclasses import dataclass
from typing import List, Set


@dataclass
class Card:
    id: int
    winning_numbers: Set[int]
    our_numbers: Set[int]

    def get_num_matches(self):
        return len(self.winning_numbers.intersection(self.our_numbers))

    def get_points(self):
        num_matches = self.get_num_matches()
        if num_matches == 0:
            return 0
        else:
            return int(math.pow(2, num_matches - 1))


def main(input_file: str, part: int):
    cards = read_cards(input_file)

    if part == 1:
        cards_count = get_cards_points(cards)
        cards_count_sum = sum(cards_count)
        print(f"The cards points are: {cards_count}. They sum {cards_count_sum}.")
        return cards_count_sum
    else:
        cards_count = get_cards_counts(cards)
        cards_count_sum = sum(cards_count)
        print(f"The final card count is: {cards_count}. They sum {cards_count_sum}.")
        return cards_count_sum


def read_cards(file_path: str) -> List[Card]:
    cards = []
    with open(file_path, "r") as f:
        for line in f:
            line = line.rstrip()
            line = line.split(":", 1)

            card_id = line[0]
            card_id = int(card_id.replace("Card ", ""))

            winning_numbers, our_numbers = line[1].split(" | ", 1)
            winning_numbers = set([int(n) for n in winning_numbers.replace("  ", " ").strip().split(" ")])
            our_numbers = set([int(n) for n in our_numbers.replace("  ", " ").strip().split(" ")])
            cards.append(Card(card_id, winning_numbers, our_numbers))

    return cards


def get_cards_points(cards: List[Card]) -> List[int]:
    """Returns the number of points that each card grants, based on the initial understanding of the game."""
    return [c.get_points() for c in cards]


def get_cards_counts(cards: List[Card]) -> List[int]:
    """Returns the total number of cards of each ID that you end up with, based on the real rules of the game."""
    cards_counts = [1] * len(cards)
    for card_id, card in enumerate(cards):
        card_count = cards_counts[card_id]
        for i in range(card.get_num_matches()):
            new_card_id = card_id + i + 1
            cards_counts[new_card_id] = cards_counts[new_card_id] + card_count

    return cards_counts


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input-file", required=True)
    parser.add_argument("-p", "--part", type=int, choices=[1, 2], required=True)
    args = parser.parse_args()

    main(args.input_file, args.part)
