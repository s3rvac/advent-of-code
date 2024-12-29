#
# Advent of Code 2023, day 23
#

import dataclasses
import textwrap
import unittest


@dataclasses.dataclass
class Hike:
    i: int
    j: int
    steps: int
    visited: set

    def step_to(self, i, j):
        visited = self.visited | {(self.i, self.j)}
        return Hike(i, j, self.steps + 1, visited)


def read_input():
    with open('input.txt', encoding='utf-8') as f:
        return f.read()


def parse_input(input):
    return [list(line) for line in input.strip().split('\n')]


def get_longest_hike_length(map):
    # We perform a depth-first search (but a breadth-first search would work as
    # well) and store the length of each hike. Then, we return the length of
    # the longest hike.
    longest_hike_length = 0

    # The end is always in the last row and second-to-last column.
    END_I_J = len(map) - 1, len(map[-1]) - 2

    # The start is always in the first row and second column.
    hikes_to_check = [Hike(i=0, j=1, steps=0, visited=set())]

    while hikes_to_check:
        hike = hikes_to_check.pop()
        for ix, jx in [(0, +1), (1, 0), (-1, 0), (0, -1)]:
            i = hike.i + ix
            j = hike.j + jx
            if (
                i < 0
                or i >= len(map)
                or j < 0
                or j >= len(map[0])
                or map[i][j] == '#'
                or (i, j) in hike.visited
            ):
                continue

            if (i, j) == END_I_J:
                longest_hike_length = max(hike.steps + 1, longest_hike_length)
                continue

            hikes_to_check.append(hike.step_to(i, j))

    return longest_hike_length


def run_program(input):
    map = parse_input(input)
    return get_longest_hike_length(map)


if __name__ == '__main__':
    result = run_program(read_input())
    print(result)


class Tests(unittest.TestCase):
    def test_program_returns_correct_result_for_my_input1(self):
        input = textwrap.dedent(
            """
            #.#
            #.#
            #.#
            """
        )

        result = run_program(input)

        self.assertEqual(result, 2)

    def test_program_returns_correct_result_for_my_input2(self):
        input = textwrap.dedent(
            """
            #.###
            #...#
            #...#
            ###.#
            """
        )

        result = run_program(input)

        self.assertEqual(result, 7)

    def test_program_returns_correct_result_for_my_input3(self):
        input = textwrap.dedent(
            """
            #.###
            #.>.#
            #.>.#
            #.>.#
            ###.#
            """
        )

        result = run_program(input)

        self.assertEqual(result, 10)

    def test_program_returns_correct_result_for_example_input(self):
        input = textwrap.dedent(
            """
            #.#####################
            #.......#########...###
            #######.#########.#.###
            ###.....#.>.>.###.#.###
            ###v#####.#v#.###.#.###
            ###.>...#.#.#.....#...#
            ###v###.#.#.#########.#
            ###...#.#.#.......#...#
            #####.#.#.#######.#.###
            #.....#.#.#.......#...#
            #.#####.#.#.#########v#
            #.#...#...#...###...>.#
            #.#.#v#######v###.###v#
            #...#.>.#...>.>.#.###.#
            #####v#.#.###v#.#.###.#
            #.....#...#...#.#.#...#
            #.#########.###.#.#.###
            #...###...#...#...#.###
            ###.###.#.###v#####v###
            #...#...#.#.>.>.#.>.###
            #.###.###.#.###.#.#v###
            #.....###...###...#...#
            #####################.#
            """
        )

        result = run_program(input)

        self.assertEqual(result, 154)
