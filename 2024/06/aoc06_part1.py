#
# Advent of Code 2024, day 06, part 1
#

import textwrap
import unittest


def read_input():
    with open("input", encoding="utf-8") as f:
        return f.read()


def parse_input(input):
    return [list(line) for line in input.strip("\n").split("\n")]


def patrol_guard_until_she_leaves_map(map):
    def find_guard():
        for i, row in enumerate(map):
            for j, pos in enumerate(row):
                if pos == "^":
                    return i, j, -1, 0
        raise AssertionError("no guard found in map")

    def is_guard_inside_map(i, j):
        return 0 <= i < len(map) and 0 <= j < len(map[i])

    def move_guard(i, j, dir_i, dir_j):
        map[i][j] = "X"
        while (
            is_guard_inside_map(i + dir_i, j + dir_j)
            and map[i + dir_i][j + dir_j] == "#"
        ):
            if (dir_i, dir_j) == (-1, 0):
                dir_i, dir_j = 0, 1
            elif (dir_i, dir_j) == (0, 1):
                dir_i, dir_j = 1, 0
            elif (dir_i, dir_j) == (1, 0):
                dir_i, dir_j = 0, -1
            else:
                dir_i, dir_j = -1, 0
        next_i, next_j = i + dir_i, j + dir_j
        return next_i, next_j, dir_i, dir_j

    i, j, dir_i, dir_j = find_guard()
    while is_guard_inside_map(i, j):
        i, j, dir_i, dir_j = move_guard(i, j, dir_i, dir_j)


def count_positions_visited_by_guard(map):
    return sum(row.count("X") for row in map)


def run_program(input):
    map = parse_input(input)
    patrol_guard_until_she_leaves_map(map)
    return count_positions_visited_by_guard(map)


if __name__ == "__main__":
    result = run_program(read_input())
    print(result)


class Tests(unittest.TestCase):
    def test_program_returns_correct_result_for_example_input(self):
        input = textwrap.dedent(
            """
            ....#.....
            .........#
            ..........
            ..#.......
            .......#..
            ..........
            .#..^.....
            ........#.
            #.........
            ......#...
            """
        )

        result = run_program(input)

        self.assertEqual(result, 41)
