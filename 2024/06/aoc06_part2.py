#
# Advent of Code 2024, day 06, part 2
#

import copy
import textwrap
import unittest


def read_input():
    with open("input", encoding="utf-8") as f:
        return f.read()


def parse_input(input):
    return [list(line) for line in input.strip("\n").split("\n")]


def find_guard(map):
    for i, row in enumerate(map):
        for j, pos in enumerate(row):
            if pos == "^":
                return i, j, -1, 0
    raise AssertionError("no guard found in map")


def move_guard_until_exit_or_loop(map, i, j, dir_i, dir_j):
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

    visited_configs = set()
    while is_guard_inside_map(i, j):
        config = (i, j, dir_i, dir_j)
        if config in visited_configs:
            return "loop"
        visited_configs.add(config)

        i, j, dir_i, dir_j = move_guard(i, j, dir_i, dir_j)

    return "exit"


def count_possible_obstruction_placements_for_loop(map):
    i, j, dir_i, dir_j = find_guard(map)

    # Get a solution to part 1 (i.e. move the guard until she reaches an exit)
    # and use that to prune the space of possible obstacle placements as it
    # only makes sense to check positions reachable from the original
    # configuration.
    move_guard_until_exit_or_loop(map, i, j, dir_i, dir_j)

    # Check all the viable positions to see at how many places we can put an
    # obstacle to make the guard end in a loop.
    placement_count = 0
    for m in range(len(map)):
        for n in range(len(map[m])):
            if (m, n) != (i, j) and map[m][n] == "X":
                map_copy = copy.deepcopy(map)
                map_copy[m][n] = "#"
                result = move_guard_until_exit_or_loop(map_copy, i, j, dir_i, dir_j)
                if result == "loop":
                    placement_count += 1
    return placement_count


def run_program(input):
    map = parse_input(input)
    return count_possible_obstruction_placements_for_loop(map)


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

        self.assertEqual(result, 6)
