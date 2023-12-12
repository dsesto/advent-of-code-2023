"""
--- Day 11: Cosmic Expansion ---
The researcher has collected a bunch of data and compiled the data into a single giant image (your puzzle input).
The image includes empty space (.) and galaxies (#). The researcher is trying to figure out the sum of the lengths of
the shortest path between every pair of galaxies. However, there's a catch: the universe expanded in the time it took
the light from those galaxies to reach the observatory. Due to something involving gravitational effects, only some
space expands. In fact, the result is that any rows or columns that contain no galaxies should all actually be twice
as big.
Expand the universe, then find the length of the shortest path between every pair of galaxies. What is the sum of these
lengths?

*ANSWER: 9329143*

--- Part Two ---
The galaxies are much older (and thus much farther apart) than the researcher initially estimated. Now, instead of the
expansion you did before, make each empty row or column one million times larger. That is, each empty row should be
replaced with 1000000 empty rows, and each empty column should be replaced with 1000000 empty columns.
What is the sum of these lengths?

*ANSWER: 710674907809*
"""
import argparse


def main(input_file: str, part: int, expansion: int = 1000000):
    if part == 1:
        sky = read_sky(input_file)
        expanded_sky = expand_universe(sky)
        galaxies = find_galaxies(expanded_sky)
        galaxies_distances = find_distances_between_galaxies(galaxies)
        # Divide sum of distances by 2 because each pair is counted twice
        total_distance_between_galaxies = int(sum([sum(d) for d in galaxies_distances]) / 2)
        print(f"Found galaxy distances {galaxies_distances}. The total is {total_distance_between_galaxies}.")
        return total_distance_between_galaxies
    else:
        # For part 2, instead of doing an explicit expansion of the universe, let's replace
        # spaces (.) with numbers (1) to represent how much space there is between galaxies.
        # If a space is expanded, its number will increment.
        sky = read_sky(input_file)
        expanded_sky = expand_universe_mathematically(sky, expansion)
        galaxies = find_galaxies(expanded_sky)
        galaxies_distances = find_distances_between_galaxies_mathematically(expanded_sky, galaxies)
        # Divide sum of distances by 2 because each pair is counted twice
        total_distance_between_galaxies = int(sum([sum(d) for d in galaxies_distances]) / 2)
        print(f"Found galaxy distances {galaxies_distances}. The total is {total_distance_between_galaxies}.")
        return total_distance_between_galaxies


def read_sky(file_path: str) -> list[list[str]]:
    sky = []
    with open(file_path, "r") as f:
        for row, line in enumerate(f):
            line = line.rstrip()
            sky.append([str(c) for c in line])

    return sky


def expand_universe(matrix: list[list[str]]) -> list[list[str]]:
    """Expands the universe by duplicating empty rows."""

    def expand_rows(m):
        empty_row = ["."] * len(m[0])

        expanded_m = []
        for idx, row in enumerate(m):
            expanded_m.append(row)
            if row == empty_row:
                expanded_m.append(row)

        return expanded_m

    expanded_matrix = expand_rows(matrix)
    expanded_matrix = transpose_matrix(expanded_matrix)
    expanded_matrix = expand_rows(expanded_matrix)
    expanded_matrix = transpose_matrix(expanded_matrix)
    return expanded_matrix


def expand_universe_mathematically(matrix: list[list[str]], expansion=1000000) -> list[list[str]]:
    """Replace spaces (.) with distances (1); then augment distances via expansion."""

    def expand_rows(m, axis: int):
        """Axis represents which axis to expand: rows (0) or columns (1)"""

        def is_empty_row(r):
            for e in r:
                if e == "#":
                    return False
            return True

        expanded_m = []
        for idx, row in enumerate(m):
            if is_empty_row(row):
                if axis == 0:
                    expanded_m.append([(e[0] * expansion, e[1]) for e in row])
                else:
                    expanded_m.append([(e[0], e[1] * expansion) for e in row])
            else:
                expanded_m.append(row)

        return expanded_m

    expanded_matrix = [
        [matrix[i][j] if matrix[i][j] == "#" else (1, 1) for j in range(len(matrix))] for i in range(len(matrix[0]))
    ]
    expanded_matrix = expand_rows(expanded_matrix, axis=1)
    expanded_matrix = transpose_matrix(expanded_matrix)
    expanded_matrix = expand_rows(expanded_matrix, axis=0)
    expanded_matrix = transpose_matrix(expanded_matrix)
    return expanded_matrix


def transpose_matrix(matrix: list[list[str]]) -> list[list[str]]:
    return [[matrix[j][i] for j in range(len(matrix))] for i in range(len(matrix[0]))]


def find_galaxies(matrix: list[list[str]]) -> list[tuple[int, int]]:
    galaxies_locations = []
    for row_idx, row in enumerate(matrix):
        for col_idx, col in enumerate(row):
            if col == "#":
                galaxies_locations.append((row_idx, col_idx))

    return galaxies_locations


def find_distances_between_galaxies(galaxies_locations: list[tuple[int, int]]) -> list[list[int]]:
    distances = []
    for src_galaxy in galaxies_locations:
        galaxy_distances = []
        for dst_galaxy in galaxies_locations:
            dist = abs(src_galaxy[0] - dst_galaxy[0]) + abs(src_galaxy[1] - dst_galaxy[1])
            if dist != 0:
                # Ignore distance with itself
                galaxy_distances.append(dist)
        distances.append(galaxy_distances)
    return distances


def find_distances_between_galaxies_mathematically(sky: list[list[str]], galaxies_locations: list[tuple[int, int]]) -> \
        list[list[int]]:
    """
    TODO: This piece of code is tremendously slow (>2min for the final input).
     A different idea to test would be to reimplement "find_galaxies()" so that distances already take into account
     the spaces. Then, we could use the normal "find_distances_between_galaxies()".
    """
    distances = []
    for src_galaxy in galaxies_locations:
        galaxy_distances = []
        for dst_galaxy in galaxies_locations:
            dist_x = 0
            dist_y = 0
            if src_galaxy[1] != dst_galaxy[1]:
                dist_x = sum([1] + [dist[0] if dist != "#" else 1 for i, dist in enumerate(sky[src_galaxy[0]])
                                    if i in range(min(src_galaxy[1], dst_galaxy[1]) + 1,
                                                  max(src_galaxy[1], dst_galaxy[1]))])
            if src_galaxy[0] != dst_galaxy[0]:
                dist_y = sum(
                    [1] + [dist[1] if dist != "#" else 1 for i, dist in enumerate(transpose_matrix(sky)[src_galaxy[1]])
                           if i in range(min(src_galaxy[0], dst_galaxy[0]) + 1,
                                         max(src_galaxy[0], dst_galaxy[0]))])
            dist = dist_x + dist_y
            if dist > 0:
                # Ignore distance with itself
                galaxy_distances.append(dist)
        distances.append(galaxy_distances)
    return distances


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input-file", required=True)
    parser.add_argument("-p", "--part", type=int, choices=[1, 2], required=True)
    parser.add_argument("-e", "--expansion", type=int, default=1000000)
    args = parser.parse_args()

    main(args.input_file, args.part, args.expansion)
