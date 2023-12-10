"""
--- Day 10: Pipe Maze ---
You make a quick sketch of all of the surface pipes you can see (your puzzle input). Based on the acoustics of the
animal's scurrying, you're confident the pipe that contains the animal is one large, continuous loop. Unfortunately,
there are also many pipes that aren't connected to the loop!
"S" is the starting position of the animal; there is a pipe on this tile, but your sketch doesn't show what shape the
pipe has.
How many steps along the loop does it take to get from the starting position to the point farthest from the starting
position?

*ANSWER: 6875*

--- Part Two ---
You quickly reach the farthest point of the loop, but the animal never emerges. Maybe its nest is within the area
enclosed by the loop?
Figure out whether you have time to search for the nest by calculating the area within the loop. How many tiles are
enclosed by the loop?

*ANSWER: 471*
"""
import argparse
import math
from enum import Enum
from typing import List, Tuple, Optional


class Direction(str, Enum):
    UP = "up"
    DOWN = "down"
    LEFT = "left"
    RIGHT = "right"


def main(input_file: str, part: int):
    maze, starting_pos = read_maze(input_file)
    starting_symbol, starting_direction = find_starting_symbol(maze, starting_pos)
    maze[starting_pos[0]][starting_pos[1]] = starting_symbol  # Replace S with starting symbol

    next_pos, next_symbol, next_direction = starting_pos, starting_symbol, starting_direction
    maze_positions = [next_pos]
    while next_pos is not None:
        next_pos, next_direction = get_next_maze_position(next_symbol, next_pos, next_direction)
        next_symbol = maze[next_pos[0]][next_pos[1]]
        if next_pos == starting_pos:
            next_pos = None
        else:
            maze_positions.append(next_pos)
    # For visibility purposes, replace non-maze positions with dots '.'
    for row in range(len(maze)):
        for col in range(len(maze[row])):
            if not (row, col) in maze_positions:
                maze[row][col] = "."

    max_distance = math.ceil(len(maze_positions) / 2)
    print_maze(maze)
    print(f"Found maze with starting symbol '{starting_symbol}'. The loop has length {len(maze_positions)}, so "
          f"the maximum distance inside the loop is {max_distance}.")

    if part == 1:
        return max_distance

    # Part 2
    i_found = cover_areas(maze)
    print_maze(maze)
    print(f"Found {i_found} inside areas.")
    return i_found


def read_maze(file_path: str) -> Tuple[List[List[str]], Tuple[int, int]]:
    maze = []
    starting_pos_row = 0
    starting_pos_col = 0
    with open(file_path, "r") as f:
        for row, line in enumerate(f):
            line = line.rstrip()
            maze.append([c for c in line])
            if "S" in line:
                starting_pos_row = row
                starting_pos_col = line.find("S")

    return maze, (starting_pos_row, starting_pos_col)


def find_starting_symbol(maze: List[List[str]], starting_pos: Tuple[int, int]) -> Tuple[str, Direction]:
    """Determines which is the symbol that hides behind the starting 'S'."""
    left_symbol = maze[starting_pos[0]][starting_pos[1] - 1]
    right_symbol = maze[starting_pos[0]][starting_pos[1] + 1]
    up_symbol = maze[starting_pos[0] - 1][starting_pos[1]]
    down_symbol = maze[starting_pos[0] + 1][starting_pos[1]]

    directions = set()
    if left_symbol in ("-", "L", "F"):
        directions.add(Direction.LEFT)
    if right_symbol in ("-", "J", "7"):
        directions.add(Direction.RIGHT)
    if up_symbol in ("|", "F", "7"):
        directions.add(Direction.UP)
    if down_symbol in ("|", "L", "J"):
        directions.add(Direction.DOWN)

    if len(directions) != 2:
        raise ValueError("Error mapping starting point S.")

    if len(directions.intersection({Direction.LEFT, Direction.RIGHT})) == 2:
        return "-", Direction.RIGHT
    elif len(directions.intersection({Direction.UP, Direction.DOWN})) == 2:
        return "|", Direction.DOWN
    elif len(directions.intersection({Direction.RIGHT, Direction.UP})) == 2:
        return "L", Direction.DOWN
    elif len(directions.intersection({Direction.LEFT, Direction.UP})) == 2:
        return "J", Direction.DOWN
    elif len(directions.intersection({Direction.LEFT, Direction.DOWN})) == 2:
        return "7", Direction.UP
    elif len(directions.intersection({Direction.RIGHT, Direction.DOWN})) == 2:
        return "F", Direction.UP


def get_next_maze_position(symbol: str, current_position: Tuple[int, int], current_direction: Direction) -> \
        (Tuple[Optional[Tuple[int, int]], Optional[Direction]]):
    """
    | is a vertical pipe connecting north and south.
    - is a horizontal pipe connecting east and west.
    L is a 90-degree bend connecting north and east.
    J is a 90-degree bend connecting north and west.
    7 is a 90-degree bend connecting south and west.
    F is a 90-degree bend connecting south and east.
    . is ground; there is no pipe in this tile.
    """
    next_position, next_direction = None, None
    if symbol == "|":
        index_increment = 1 if current_direction in (Direction.DOWN, Direction.RIGHT) else -1
        next_direction = current_direction
        next_position = (current_position[0] + index_increment, current_position[1])
    elif symbol == "-":
        index_increment = 1 if current_direction in (Direction.DOWN, Direction.RIGHT) else -1
        next_direction = current_direction
        next_position = (current_position[0], current_position[1] + index_increment)
    elif symbol == "L":
        if current_direction == Direction.DOWN:
            next_direction = Direction.RIGHT
            next_position = (current_position[0], current_position[1] + 1)
        elif current_direction == Direction.LEFT:
            next_direction = Direction.UP
            next_position = (current_position[0] - 1, current_position[1])
        else:
            raise ValueError(f"Invalid {current_direction=} for {symbol=}.")
    elif symbol == "J":
        if current_direction == Direction.DOWN:
            next_direction = Direction.LEFT
            next_position = (current_position[0], current_position[1] - 1)
        elif current_direction == Direction.RIGHT:
            next_direction = Direction.UP
            next_position = (current_position[0] - 1, current_position[1])
        else:
            raise ValueError(f"Invalid {current_direction=} for {symbol=}.")
    elif symbol == "7":
        if current_direction == Direction.UP:
            next_direction = Direction.LEFT
            next_position = (current_position[0], current_position[1] - 1)
        elif current_direction == Direction.RIGHT:
            next_direction = Direction.DOWN
            next_position = (current_position[0] + 1, current_position[1])
    elif symbol == "F":
        if current_direction == Direction.UP:
            next_direction = Direction.RIGHT
            next_position = (current_position[0], current_position[1] + 1)
        elif current_direction == Direction.LEFT:
            next_direction = Direction.DOWN
            next_position = (current_position[0] + 1, current_position[1])
        else:
            raise ValueError(f"Invalid {current_direction=} for {symbol=}.")

    return next_position, next_direction


def print_maze(maze: List[List[str]]):
    for row in maze:
        print("".join(row))


def cover_areas(maze: List[List[str]]) -> int:
    """
    Paint areas as O (Outside) or I (Inside) depending on whether points are outside or inside the shape.
    To determine whether a point is O or I, we can make use of parity. If an odd amount of walls (|, J, L) was found
    before reaching the point ".", it will be an I; if the amount is even, it will be an O.
    """
    i_found = 0
    for row_idx, row in enumerate(maze):
        num_walls_seen = 0
        for col_idx, c in enumerate(row):
            if c in ("|", "L", "J"):
                num_walls_seen += 1
            elif c == ".":
                if num_walls_seen % 2 == 0:
                    maze[row_idx][col_idx] = "O"
                else:
                    maze[row_idx][col_idx] = "I"
                    i_found += 1

    return i_found


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input-file", required=True)
    parser.add_argument("-p", "--part", type=int, choices=[1, 2], required=True)
    args = parser.parse_args()

    main(args.input_file, args.part)
