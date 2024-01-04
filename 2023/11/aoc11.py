#
# Advent of Code 2023, day 11
#

import itertools
import textwrap
import unittest


def read_input():
    with open('input.txt', encoding='utf-8') as f:
        return f.read()


def parse_input(input):
    return [list(line) for line in input.strip().split('\n')]


def get_shortest_paths_between_all_galaxies(universe):
    coordinates = get_coordinates_of_all_galaxies(universe)
    return [
        get_shortest_path_between_two_galaxies(c1, c2)
        for c1, c2 in itertools.combinations(coordinates, 2)
    ]


def get_coordinates_of_all_galaxies(universe):
    rows_to_expand, columns_to_expand = get_rows_and_columns_to_expand(universe)

    coordinates = []
    for x, row in enumerate(universe):
        for y, c in enumerate(row):
            if c == '#':
                coordinates.append(
                    get_galaxy_coordinates_in_expanded_universe(
                        rows_to_expand, columns_to_expand, x, y
                    )
                )
    return coordinates


def get_rows_and_columns_to_expand(universe):
    rows_to_expand = [
        i for i, row in enumerate(universe) if row.count('#') == 0
    ]

    all_columns = [[row[i] for row in universe] for i in range(len(universe[0]))]
    columns_to_expand = [
        i for i, column in enumerate(all_columns) if column.count('#') == 0
    ]

    return rows_to_expand, columns_to_expand


def get_galaxy_coordinates_in_expanded_universe(rows_to_expand, columns_to_expand, x, y):
    expansion_factor = 1_000_000

    expanded_x = 0
    for i in range(x):
        expanded_x += expansion_factor if i in rows_to_expand else 1

    expanded_y = 0
    for i in range(y):
        expanded_y += expansion_factor if i in columns_to_expand else 1

    return expanded_x, expanded_y


def get_shortest_path_between_two_galaxies(c1, c2):
    # We can move only left, right, up, and down, so the path of going all the
    # way horizontally and then vertically is the same as going "diagonally".
    # Each of the coordinates is of the form (x, y).
    return abs(c1[0] - c2[0]) + abs(c1[1] - c2[1])


def run_program(input):
    universe = parse_input(input)
    shortest_paths = get_shortest_paths_between_all_galaxies(universe)
    return sum(shortest_paths)


if __name__ == '__main__':
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
