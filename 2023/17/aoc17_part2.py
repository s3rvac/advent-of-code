#
# Advent of Code 2023, day 17, part 2
#

import heapq
import textwrap
import unittest


def read_input():
    with open("input", encoding="utf-8") as f:
        return f.read()


def parse_input(input):
    return [[int(c) for c in line] for line in input.strip().split("\n")]


def get_min_heat_loss_when_navigating_crucible(map):
    AVAILABLE_DIRECTIONS = [(1, 0), (0, 1), (-1, 0), (0, -1)]
    DESTINATION = (len(map) - 1, len(map[0]) - 1)
    MIN_STEPS = 4
    MAX_STEPS = 10

    # A priority queue, where the priority is defined by the heat loss (the
    # lower the better).
    # Format: (heat_loss, i, j, ix, jx, steps)
    q = [(0, 0, 0, 0, 0, 0)]

    # We need to maintain a set of visited configurations as to not visit the
    # same configuration twice (disregarding heat loss).
    visited = set()

    def check(heat_loss, i, j, ix, jx, steps):
        if 0 <= i < len(map) and 0 <= j < len(map[i]):
            heapq.heappush(q, (heat_loss + map[i][j], i, j, ix, jx, steps))

    while q:
        heat_loss, i, j, ix, jx, steps = heapq.heappop(q)

        if (i, j) == DESTINATION and steps >= MIN_STEPS:
            return heat_loss

        c = (i, j, ix, jx, steps)
        if c in visited:
            continue
        visited.add(c)

        # Try stepping while preserving the direction.
        if steps < MAX_STEPS and (ix, jx) != (0, 0):
            check(heat_loss, i + ix, j + jx, ix, jx, steps + 1)

        # Try stepping while changing the direction.
        if steps >= MIN_STEPS or (ix, jx) == (0, 0):
            for new_ix, new_jx in AVAILABLE_DIRECTIONS:
                if (new_ix, new_jx) != (ix, jx) and (new_ix, new_jx) != (-ix, -jx):
                    check(heat_loss, i + new_ix, j + new_jx, new_ix, new_jx, steps=1)


def run_program(input):
    map = parse_input(input)
    return get_min_heat_loss_when_navigating_crucible(map)


if __name__ == "__main__":
    result = run_program(read_input())
    print(result)


class Tests(unittest.TestCase):
    def test_program_returns_correct_result_for_example_input1(self):
        input = textwrap.dedent(
            """
            2413432311323
            3215453535623
            3255245654254
            3446585845452
            4546657867536
            1438598798454
            4457876987766
            3637877979653
            4654967986887
            4564679986453
            1224686865563
            2546548887735
            4322674655533
            """
        )

        result = run_program(input)

        self.assertEqual(result, 94)

    def test_program_returns_correct_result_for_example_input2(self):
        input = textwrap.dedent(
            """
            111111111111
            999999999991
            999999999991
            999999999991
            999999999991
            """
        )

        result = run_program(input)

        self.assertEqual(result, 71)
