#
# Advent of Code 2025, day 05, part 2
#

import itertools
import textwrap
import unittest


def read_input():
    with open("input", encoding="utf-8") as f:
        return f.read()


def parse_input(input):
    raw_ranges, _ = input.strip().split("\n\n")
    return [tuple(map(int, line.split("-"))) for line in raw_ranges.split("\n")]


def get_fresh_ingredient_count(fresh_ranges):
    # First, de-duplicate the ranges to simplify the computation of the number
    # of fresh ingredients.
    dedup_ranges = set(fresh_ranges)
    new_ranges = set()
    while new_ranges != dedup_ranges:
        new_ranges = set(dedup_ranges)
        for (min1, max1), (min2, max2) in itertools.permutations(new_ranges, 2):
            if min1 <= min2 <= max2 <= max1:
                dedup_ranges.remove((min2, max2))
                break
            elif min1 <= min2 <= max1 < max2:
                dedup_ranges.remove((min1, max1))
                dedup_ranges.remove((min2, max2))
                dedup_ranges.add((min1, max2))
                break

    # Compute the number of fresh ingredient IDs from the de-duplicate ranges.
    fresh_count = 0
    for min, max in dedup_ranges:
        fresh_count += max - min + 1
    return fresh_count


def run_program(input):
    fresh_ranges = parse_input(input)
    return get_fresh_ingredient_count(fresh_ranges)


if __name__ == "__main__":
    result = run_program(read_input())
    print(result)


class Tests(unittest.TestCase):
    def test_program_returns_correct_result_for_example_input(self):
        input = textwrap.dedent(
            """
            3-5
            10-14
            16-20
            12-18

            -
            """
        )

        result = run_program(input)

        self.assertEqual(result, 14)
