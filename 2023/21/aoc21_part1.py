#
# Advent of Code 2023, day 21, part 1
#

import textwrap
import unittest


def read_input():
    with open('input.txt', encoding='utf-8') as f:
        return f.read()


def parse_input(input):
    return [list(line) for line in input.strip().split('\n')]


def count_garden_plots_after_steps(map, steps):
    DIRECTIONS = [(0, 1), (1, 0), (-1, 0), (0, -1)]
    positions = {get_start_position(map)}

    for _ in range(steps):
        new_positions = set()
        for i, j in positions:
            for ix, jx in DIRECTIONS:
                new_i, new_j = i + ix, j + jx
                if (
                    0 <= new_i < len(map)
                    and 0 <= new_j < len(map[new_i])
                    and map[new_i][new_j] != '#'
                ):
                    new_positions.add((new_i, new_j))
        positions = new_positions

    return len(positions)


def get_start_position(map):
    for i in range(len(map)):
        for j in range(len(map[i])):
            if map[i][j] == 'S':
                return i, j
    raise AssertionError('No start position found')


def run_program(input, steps):
    map = parse_input(input)
    return count_garden_plots_after_steps(map, steps)


if __name__ == '__main__':
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
