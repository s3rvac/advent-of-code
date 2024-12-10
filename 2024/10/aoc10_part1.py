#
# Advent of Code 2024, day 10, part 1
#

import textwrap
import unittest


TRAIL_START_HEIGHT = 0
TRAIL_END_HEIGHT = 9


def read_input():
    with open("input", encoding="utf-8") as f:
        return f.read()


def parse_input(input):
    return [[int(n) for n in line] for line in input.strip().split("\n")]


def compute_trailhead_scores(map):
    def is_position_inside_map(i, j):
        return 0 <= i < len(map) and 0 <= j < len(map[i])

    def compute_trailhead_score_from_position(i, j):
        # Use depth-first search (but breadth-first search would work as well)
        # to find the score of the trailhead.
        reached_trail_ends = set()
        to_visit = [(i, j)]
        while to_visit:
            i, j = to_visit.pop()
            for ix, jx in [(0, 1), (-1, 0), (0, -1), (1, 0)]:
                new_i = i + ix
                new_j = j + jx
                if (
                    is_position_inside_map(new_i, new_j)
                    and map[new_i][new_j] == map[i][j] + 1
                ):
                    if map[new_i][new_j] < TRAIL_END_HEIGHT:
                        to_visit.append((new_i, new_j))
                    elif (new_i, new_j) not in reached_trail_ends:
                        reached_trail_ends.add((new_i, new_j))
        return len(reached_trail_ends)

    trailhead_scores = []
    for i in range(len(map)):
        for j in range(len(map[i])):
            if map[i][j] == TRAIL_START_HEIGHT:
                trailhead_scores.append(compute_trailhead_score_from_position(i, j))
    return trailhead_scores


def run_program(input):
    map = parse_input(input)
    trailhead_scores = compute_trailhead_scores(map)
    return sum(trailhead_scores)


if __name__ == "__main__":
    result = run_program(read_input())
    print(result)


class Tests(unittest.TestCase):
    def test_program_returns_correct_result_for_example_input(self):
        input = textwrap.dedent(
            """
            89010123
            78121874
            87430965
            96549874
            45678903
            32019012
            01329801
            10456732
            """
        )

        result = run_program(input)

        self.assertEqual(result, 36)
