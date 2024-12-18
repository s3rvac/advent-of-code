#
# Advent of Code 2024, day 18, part 1
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


def count_min_steps_to_reach_end_of_grid(grid_size, unavailable_positions):
    # Use a simplified version of Dijkstra's algorithm to find the shortest
    # path from the start to the end.
    UNAVAILABLE = set(unavailable_positions)
    START = (0, 0)
    END = (grid_size - 1, grid_size - 1)
    INFINITY = grid_size * grid_size

    distances = {START: 0}
    for i in range(grid_size):
        for j in range(grid_size):
            if (i, j) != START and (i, j) not in UNAVAILABLE:
                distances[(i, j)] = INFINITY

    pq = []
    heapq.heappush(pq, (0, *START))
    while pq:
        distance, i, j = heapq.heappop(pq)
        if distance > distances[(i, j)]:
            continue

        for di, dj in NEIGHBOR_DIRECTIONS:
            new_i, new_j = i + di, j + dj
            if (
                0 <= new_i < grid_size
                and 0 <= new_j < grid_size
                and (new_i, new_j) not in UNAVAILABLE
            ):
                new_distance = distance + 1
                if new_distance < distances[(new_i, new_j)]:
                    distances[(new_i, new_j)] = new_distance
                    heapq.heappush(pq, (new_distance, new_i, new_j))

    return distances[END]


def run_program(input, grid_size=71, byte_count_to_fall=1024):
    byte_positions = parse_input(input)
    return count_min_steps_to_reach_end_of_grid(
        grid_size, byte_positions[:byte_count_to_fall]
    )


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

        result = run_program(input, grid_size=7, byte_count_to_fall=12)

        self.assertEqual(result, 22)
