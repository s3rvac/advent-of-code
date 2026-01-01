#
# Advent of Code 2025, day 07, part 1
#

import textwrap
import unittest


def read_input():
    with open("input", encoding="utf-8") as f:
        return f.read()


def parse_input(input):
    return [list(line) for line in input.strip().split("\n")]


def count_beam_splits(map):
    beam_splits = 0
    beams = set()
    for i in range(0, len(map)):
        for j in range(0, len(map[i])):
            if map[i][j] == "S":
                beams.add((i, j))
            elif map[i][j] == "." and (i - 1, j) in beams:
                beams.add((i, j))
            elif map[i][j] == "^" and (i - 1, j) in beams:
                beams.add((i, j - 1))
                beams.add((i, j + 1))
                beam_splits += 1
    return beam_splits


def run_program(input):
    map = parse_input(input)
    return count_beam_splits(map)


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

        self.assertEqual(result, 21)
