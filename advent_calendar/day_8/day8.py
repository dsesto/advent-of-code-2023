"""
--- Day 8: Haunted Wasteland ---
A map contains a list of left/right instructions, and the rest of the documents seem to describe some kind of network of
labeled nodes. It seems like you're meant to use the left/right instructions to navigate the network. Perhaps if you
have the camel follow the same instructions, you can escape the haunted wasteland!
After examining the maps for a bit, two nodes stick out: AAA and ZZZ. You feel like AAA is where you are now, and you
have to follow the left/right instructions until you reach ZZZ.
If you run out of left/right instructions, repeat the whole sequence of instructions as necessary.
How many steps are required to reach ZZZ?

*ANSWER: 14893*

--- Part Two ---
If you were a ghost, you'd probably just start at every node that ends with A and follow all of the paths at the same
time until they all simultaneously end up at nodes that end with Z.
Use that instruction to simultaneously navigate away from both nodes you're currently on. Repeat this process until all
of the nodes you're currently on end with Z.
How many steps does it take before you're only on nodes that end with Z?

*ANSWER: 10241191004509*
"""
from __future__ import annotations

import argparse
import math
from typing import List, Union, Tuple


class Node:

    def __init__(self, node_id: str, left_node: str, right_node: str):
        self.id: str = node_id
        self._left_node: Union[str, Node] = left_node
        self._right_node: Union[str, Node] = right_node

    @property
    def left_node(self):
        return self._left_node

    @left_node.setter
    def left_node(self, node: Node):
        self._left_node = node

    @property
    def right_node(self):
        return self._right_node

    @right_node.setter
    def right_node(self, node: Node):
        self._right_node = node

    def move_left(self):
        return self.left_node

    def move_right(self):
        return self.right_node

    def move(self, movement: str):
        if movement == "L":
            return self.move_left()
        elif movement == "R":
            return self.move_right()
        else:
            raise ValueError(f"Invalid movement '{movement}'.")


def main(input_file: str, part: int):
    starting_nodes, path = read_map(input_file, part)
    num_steps = []
    for starting_node in starting_nodes:
        num_steps.append(traverse_map(starting_node, path, part))

    if len(num_steps) == 1:
        total_num_steps = num_steps[0]
    else:
        # For part 2, we compute the LCM to find the common point where all paths end simultaneously
        total_num_steps = math.lcm(*num_steps)

    print(f"Map traversed with steps: {num_steps}. The total is {total_num_steps} steps.")
    return total_num_steps


def read_map(file_path: str, part: int) -> Tuple[List[Node], List[str]]:
    starting_nodes = None
    path = None
    nodes = {}

    with open(file_path, "r") as f:
        for row, line in enumerate(f):
            line = line.rstrip()
            if row == 0:
                path = [c for c in line]
            elif row > 1:
                node_id, node_connections = line.split(" = ")
                node_left = node_connections.split(", ", 1)[0][1:]
                node_right = node_connections.split(", ", 1)[1][:-1]

                nodes[node_id] = Node(node_id, node_left, node_right)

    for node in list(nodes.values()):
        # Replace strings with actual references to a Node
        node.left_node = nodes[node.left_node]
        node.right_node = nodes[node.right_node]

    if part == 1:
        starting_nodes = [nodes["AAA"]]
    elif part == 2:
        starting_nodes = [n for n in list(nodes.values()) if n.id.endswith("A")]

    return starting_nodes, path


def traverse_map(starting_node: Node, path: List[str], part: int) -> int:
    ending_found = False
    ending_node = "ZZZ" if part == 1 else "Z"

    num_steps = 0
    path_length = len(path)
    current_node = starting_node
    while not ending_found:
        movement = path[num_steps % path_length]
        current_node = current_node.move(movement)
        num_steps += 1

        if current_node.id.endswith(ending_node):
            ending_found = True

    return num_steps


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input-file", required=True)
    parser.add_argument("-p", "--part", type=int, choices=[1, 2], required=True)
    args = parser.parse_args()

    main(args.input_file, args.part)
