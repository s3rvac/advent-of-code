#
# Advent of Code 2025, day 07, part 2
#

import functools
import textwrap
import unittest


def read_input():
    with open("input", encoding="utf-8") as f:
        return f.read()


def parse_input(input):
    return [list(line) for line in input.strip().split("\n")]


def count_timelines(map):
    # Use a resursive implementation with caching to speed up the computation.
    @functools.cache
    def ct(i, j):
        while i < len(map) and map[i][j] in (".", "S"):
            i += 1

        if i == len(map):
            # We have reached the end of the map.
            return 1

        # We have encountered a splitter, so count both options: (1) the beam
        # goes to the left and (2) the beam goes to the right.
        assert map[i][j] == "^"
        return ct(i, j - 1) + ct(i, j + 1)

    return ct(0, map[0].index("S"))


def run_program(input):
    map = parse_input(input)
    return count_timelines(map)


if __name__ == "__main__":
    result = run_program(read_input())
    print(result)


class Tests(unittest.TestCase):
    def test_program_returns_correct_result_for_example_input(self):
        input = textwrap.dedent(
            """
            .......S.......
            ...............
            .......^.......
            ...............
            ......^.^......
            ...............
            .....^.^.^.....
            ...............
            ....^.^...^....
            ...............
            ...^.^...^.^...
            ...............
            ..^...^.....^..
            ...............
            .^.^.^.^.^...^.
            ...............
            """
        )

        result = run_program(input)

        self.assertEqual(result, 40)
