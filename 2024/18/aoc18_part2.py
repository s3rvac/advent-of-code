#
# Advent of Code 2024, day 18, part 2
#

import heapq
import textwrap
import unittest


NEIGHBOR_DIRECTIONS = [(0, 1), (0, -1), (-1, 0), (1, 0)]


def read_input():
    with open("input", encoding="utf-8") as f:
        return f.read()


def parse_input(input):
    def parse_position(line):
        # Switch the x and y coordinates to simplify the implementation.
        x, y = line.split(",")
        return int(y), int(x)

    return [parse_position(line) for line in input.strip().split("\n")]


def is_end_reachable_from_start(grid_size, unavailable_positions):
    # Use depth-first search (breadth-first search would work as well) to check
    # if the end is reachable from the start.
    UNAVAILABLE = set(unavailable_positions)
    START = (0, 0)
    END = (grid_size - 1, grid_size - 1)

    visited = set()
    to_check = [START]
    while to_check:
        i, j = to_check.pop()
        if (i, j) == END:
            return True

        visited.add((i, j))

        for di, dj in NEIGHBOR_DIRECTIONS:
            new_i, new_j = i + di, j + dj
            if (
                0 <= new_i < grid_size
                and 0 <= new_j < grid_size
                and (new_i, new_j) not in UNAVAILABLE
                and (new_i, new_j) not in visited
            ):
                to_check.append((new_i, new_j))

    return False


def get_position_of_first_byte_that_blocks_path(grid_size, byte_positions):
    # Use binary search to quickly find the first byte that blocks the path.
    left = 1
    right = len(byte_positions) - 1
    while left <= right:
        i = (left + right) // 2
        if is_end_reachable_from_start(grid_size, byte_positions[: i + 1]):
            left = i + 1
        else:
            if is_end_reachable_from_start(grid_size, byte_positions[:i]):
                return byte_positions[i]
            right = i - 1

    raise AssertionError("no byte blocks the path")


def run_program(input, grid_size=71):
    byte_positions = parse_input(input)
    x, y = get_position_of_first_byte_that_blocks_path(grid_size, byte_positions)
    # We need to switch the x and y coordinates here as we have switched them
    # when parsing the input to simplify the implementation.
    return f"{y},{x}"


if __name__ == "__main__":
    result = run_program(read_input())
    print(result)


class Tests(unittest.TestCase):
    def test_program_returns_correct_result_for_example_input(self):
        input = textwrap.dedent(
            """
            5,4
            4,2
            4,5
            3,0
            2,1
            6,3
            2,4
            1,5
            0,6
            3,3
            2,6
            5,1
            1,2
            5,5
            2,5
            6,5
            1,4
            0,4
            6,4
            1,1
            6,1
            1,0
            0,5
            1,6
            2,0
            """
        )

        result = run_program(input, grid_size=7)

        self.assertEqual(result, "6,1")
