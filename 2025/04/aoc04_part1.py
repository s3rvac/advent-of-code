#
# Advent of Code 2025, day 04, part 1
#

import textwrap
import unittest


NEIGHBOR_DIRECTIONS = [
    (-1, -1),
    (-1, 0),
    (-1, 1),
    (0, -1),
    (0, 1),
    (1, -1),
    (1, 0),
    (1, 1),
]


def read_input():
    with open("input", encoding="utf-8") as f:
        return f.read()


def parse_input(input):
    return [list(line) for line in input.strip().split()]


def get_number_of_rolls_accessible_by_forklift(diagram):
    def is_roll_accessible(i, j):
        adjacent_rolls = 0
        for di, dj in NEIGHBOR_DIRECTIONS:
            if (
                0 <= (i + di) < len(diagram[0])
                and 0 <= (j + dj) < len(diagram)
                and diagram[i + di][j + dj] == "@"
            ):
                adjacent_rolls += 1
        return adjacent_rolls < 4

    accessible_rolls = 0
    for i in range(0, len(diagram[0])):
        for j in range(0, len(diagram)):
            if diagram[i][j] == "@":
                if is_roll_accessible(i, j):
                    accessible_rolls += 1
    return accessible_rolls


def run_program(input):
    diagram = parse_input(input)
    return get_number_of_rolls_accessible_by_forklift(diagram)


if __name__ == "__main__":
    result = run_program(read_input())
    print(result)


class Tests(unittest.TestCase):
    def test_program_returns_correct_result_for_example_input(self):
        input = textwrap.dedent(
            """
            ..@@.@@@@.
            @@@.@.@.@@
            @@@@@.@.@@
            @.@@@@..@.
            @@.@@@@.@@
            .@@@@@@@.@
            .@.@.@.@@@
            @.@@@.@@@@
            .@@@@@@@@.
            @.@.@@@.@.
            """
        )

        result = run_program(input)

        self.assertEqual(result, 13)
