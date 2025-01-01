#
# Advent of Code 2023, day 11, part 2
#

import itertools
import textwrap
import unittest


EXPANSION_FACTOR = 1_000_000


def read_input():
    with open("input", encoding="utf-8") as f:
        return f.read()


def parse_input(input):
    return [list(line) for line in input.strip().split("\n")]


def get_shortest_paths_between_all_galaxies(universe):
    coordinates = get_coordinates_of_all_galaxies(universe)
    return [
        get_shortest_path_between_two_galaxies(c1, c2)
        for c1, c2 in itertools.combinations(coordinates, 2)
    ]


def get_coordinates_of_all_galaxies(universe):
    rows_to_expand, cols_to_expand = get_rows_and_cols_to_expand(universe)

    coordinates = []
    for x, row in enumerate(universe):
        for y, c in enumerate(row):
            if c == "#":
                coordinates.append(
                    get_galaxy_coordinates_in_expanded_universe(
                        rows_to_expand, cols_to_expand, x, y
                    )
                )
    return coordinates


def get_rows_and_cols_to_expand(universe):
    rows_to_expand = [i for i, row in enumerate(universe) if row.count("#") == 0]
    cols_to_expand = [i for i, col in enumerate(zip(*universe)) if col.count("#") == 0]
    return rows_to_expand, cols_to_expand


def get_galaxy_coordinates_in_expanded_universe(rows_to_expand, cols_to_expand, x, y):
    expanded_x = sum(EXPANSION_FACTOR if i in rows_to_expand else 1 for i in range(x))
    expanded_y = sum(EXPANSION_FACTOR if j in cols_to_expand else 1 for j in range(y))
    return expanded_x, expanded_y


def get_shortest_path_between_two_galaxies(c1, c2):
    # Since we are only able to move left/right/up/down, the shortest path is
    # the taxicab distance: https://en.wikipedia.org/wiki/Taxicab_geometry.
    return abs(c1[0] - c2[0]) + abs(c1[1] - c2[1])


def run_program(input):
    universe = parse_input(input)
    return sum(get_shortest_paths_between_all_galaxies(universe))


if __name__ == "__main__":
    result = run_program(read_input())
    print(result)


class Tests(unittest.TestCase):
    def test_program_returns_correct_result_for_example_input(self):
        input = textwrap.dedent(
            """
            ...#......
            .......#..
            #.........
            ..........
            ......#...
            .#........
            .........#
            ..........
            .......#..
            #...#.....
            """
        )

        result = run_program(input)

        self.assertEqual(result, 82000210)
