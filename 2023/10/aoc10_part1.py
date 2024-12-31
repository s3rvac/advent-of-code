#
# Advent of Code 2023, day 10, part 1
#

import collections
import textwrap
import unittest


def read_input():
    with open("input", encoding="utf-8") as f:
        return f.read()


def parse_input(input):
    return [list(line) for line in input.strip().split("\n")]


def get_number_of_steps_to_reach_farthest_position_in_loop(grid):
    start = find_start_position(grid)
    replace_start_position_with_pipe(start, grid)

    # Do a breadth-first search from the starting position to find the loop and
    # the number of steps that are required to reach its farthest position.
    visited = set()
    to_check = collections.deque([start])
    while to_check:
        curr = to_check.popleft()
        visited.add((curr))
        for new in get_next_positions(curr, grid):
            if new not in visited:
                to_check.append(new)

    # Since we are in a loop, we can just return the half of the number of
    # visited positions to get the number of steps that are required to reach
    # its farthest position.
    return len(visited) // 2


def find_start_position(grid):
    for i, line in enumerate(grid):
        for j, pipe in enumerate(line):
            if pipe == "S":
                return i, j
    raise AssertionError("no start position")


def replace_start_position_with_pipe(start, grid):
    i, j = start
    if grid[i - 1][j] in ["|", "7", "F"] and grid[i + 1][j] in ["|", "L", "J"]:
        grid[i][j] = "|"
    elif grid[i][j - 1] in ["-", "L", "F"] and grid[i][j + 1] in ["-", "J", "7"]:
        grid[i][j] = "-"
    elif grid[i - 1][j] in ["|", "7", "F"] and grid[i][j + 1] in ["-", "J", "7"]:
        grid[i][j] = "L"
    elif grid[i - 1][j] in ["|", "7", "F"] and grid[i][j - 1] in ["-", "L", "F"]:
        grid[i][j] = "J"
    elif grid[i][j - 1] in ["-", "L", "F"] and grid[i + 1][j] in ["|", "L", "J"]:
        grid[i][j] = "7"
    else:
        grid[i][j] = "F"


def get_next_positions(current, grid):
    # Based on the pipe at the current position in the grid, return the two
    # positions that connect to the pipe.
    i, j = current
    next_positions_for_pipe = {
        "|": [(i - 1, j), (i + 1, j)],
        "-": [(i, j - 1), (i, j + 1)],
        "L": [(i - 1, j), (i, j + 1)],
        "J": [(i - 1, j), (i, j - 1)],
        "7": [(i, j - 1), (i + 1, j)],
        "F": [(i, j + 1), (i + 1, j)],
    }
    return next_positions_for_pipe[grid[i][j]]


def run_program(input):
    grid = parse_input(input)
    return get_number_of_steps_to_reach_farthest_position_in_loop(grid)


if __name__ == "__main__":
    result = run_program(read_input())
    print(result)


class Tests(unittest.TestCase):
    def test_program_returns_correct_result_for_first_example_input(self):
        input = textwrap.dedent(
            """
            -L|F7
            7S-7|
            L|7||
            -L-J|
            L|-JF
            """
        )

        result = run_program(input)

        self.assertEqual(result, 4)

    def test_program_returns_correct_result_for_second_example_input(self):
        input = textwrap.dedent(
            """
            7-F7-
            .FJ|7
            SJLL7
            |F--J
            LJ.LJ
            """
        )

        result = run_program(input)

        self.assertEqual(result, 8)
