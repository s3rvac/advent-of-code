#
# Advent of Code 2023, day 21, part 1
#

import textwrap
import unittest


DIRECTIONS = [(0, 1), (1, 0), (-1, 0), (0, -1)]


def read_input():
    with open("input", encoding="utf-8") as f:
        return f.read()


def parse_input(input):
    return [list(line) for line in input.strip().split("\n")]


def count_garden_plots_after_steps(map, steps):
    positions = {get_start_position(map)}

    for _ in range(steps):
        new_positions = set()
        for i, j in positions:
            for ix, jx in DIRECTIONS:
                ni, nj = i + ix, j + jx
                if 0 <= ni < len(map) and 0 <= nj < len(map[ni]) and map[ni][nj] != "#":
                    new_positions.add((ni, nj))
        positions = new_positions

    return len(positions)


def get_start_position(map):
    for i in range(len(map)):
        for j in range(len(map[i])):
            if map[i][j] == "S":
                return i, j

    raise AssertionError("no start position found")


def run_program(input, steps):
    map = parse_input(input)
    return count_garden_plots_after_steps(map, steps)


if __name__ == "__main__":
    result = run_program(read_input(), steps=64)
    print(result)


class Tests(unittest.TestCase):
    def test_program_returns_correct_result_for_example_input(self):
        input = textwrap.dedent(
            """
            ...........
            .....###.#.
            .###.##..#.
            ..#.#...#..
            ....#.#....
            .##..S####.
            .##..#...#.
            .......##..
            .##.#.####.
            .##..##.##.
            ...........
            """
        )

        result = run_program(input, steps=6)

        self.assertEqual(result, 16)
