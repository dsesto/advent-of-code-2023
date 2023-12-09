"""
--- Day 7: Camel Cards ---
Camel Cards is sort of similar to poker. In Camel Cards, you get a list of hands, and your goal is to order them based
on the strength of each hand. A hand consists of five cards labeled one of A, K, Q, J, T, 9, 8, 7, 6, 5, 4, 3, or 2.
The relative strength of each card follows this order, where A is the highest and 2 is the lowest.
Every hand is exactly one type. From strongest to weakest, they are [the same as in poker].
If two hands have the same type, a second ordering rule takes effect. Start by comparing the first card in each hand.
Each hand wins an amount equal to its bid multiplied by its rank, where the weakest hand gets rank 1.
Find the rank of every hand in your set. What are the total winnings?

*ANSWER: 249726565*

--- Part Two ---
Now, J cards are jokers - wildcards that can act like whatever card would make the hand the strongest type possible.
To balance this, J cards are now the weakest individual cards, weaker even than 2. The other cards stay in the same
order: A, K, Q, T, 9, 8, 7, 6, 5, 4, 3, 2, J.
Using the new joker rule, find the rank of every hand in your set. What are the new total winnings?

*ANSWER: 251135960*
"""
import argparse
from dataclasses import dataclass, field
from typing import List

strengths_part1 = ["2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K", "A"]
strengths_part2 = ["J", "2", "3", "4", "5", "6", "7", "8", "9", "T", "Q", "K", "A"]


@dataclass
class Hand:
    cards: List[str]
    bid: int
    type: int = 0
    cards_strengths: List[int] = field(default_factory=lambda: [])
    rank: int = 1

    def set_strength(self, part: int):
        # Compute card type
        cards_groups = {}
        for card in self.cards:
            if card not in cards_groups:
                cards_groups[card] = 0
            cards_groups[card] += 1

        if part == 2 and "J" in cards_groups and cards_groups["J"] < 5:
            # Replace J for the highest-count letter
            num_j = cards_groups["J"]
            del cards_groups["J"]
            cards_groups = dict(sorted(cards_groups.items(), key=lambda x: -x[1]))
            cards_groups[list(cards_groups.keys())[0]] += num_j

        cards_groups = list(cards_groups.values())

        if 5 in cards_groups:
            self.type = 6
        elif 4 in cards_groups:
            self.type = 5
        elif 3 in cards_groups and 2 in cards_groups:
            self.type = 4
        elif 3 in cards_groups:
            self.type = 3
        elif cards_groups.count(2) == 2:
            self.type = 2
        elif 2 in cards_groups:
            self.type = 1
        else:
            self.type = 0

        # Compute individual card strengths
        strengths = strengths_part1 if part == 1 else strengths_part2
        self.cards_strengths = [strengths.index(c) for c in self.cards]

        return self

    def set_rank(self, rank):
        self.rank = rank


def main(input_file: str, part: int):
    hands = read_hands(input_file, part)

    total_winnings = compute_total_winnings(hands)
    total_winnings_sum = sum(total_winnings)
    print(f"Total winnings are: {total_winnings}. Their sum is {total_winnings_sum}.")

    return total_winnings_sum


def read_hands(file_path: str, part: int) -> List[Hand]:
    hands = []

    with open(file_path, "r") as f:
        for line in f:
            line = line.rstrip().split()
            hands.append(Hand(
                [c for c in line[0]],
                int(line[1]),
            ).set_strength(part))

    return hands


def compute_total_winnings(hands: List[Hand]):
    sorted_hands = sorted(hands, key=lambda h: (h.type, h.cards_strengths))
    total_winnings = [(idx + 1) * h.bid for idx, h in enumerate(sorted_hands)]
    return total_winnings


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input-file", required=True)
    parser.add_argument("-p", "--part", type=int, choices=[1, 2], required=True)
    args = parser.parse_args()

    main(args.input_file, args.part)
