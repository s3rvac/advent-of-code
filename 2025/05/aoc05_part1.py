#
# Advent of Code 2025, day 05, part 1
#

import textwrap
import unittest


def read_input():
    with open("input", encoding="utf-8") as f:
        return f.read()


def parse_input(input):
    p1, p2 = input.strip().split("\n\n")
    return (
        [tuple(map(int, line.split("-"))) for line in p1.split("\n")],
        [int(n) for n in p2.split("\n")],
    )


def get_fresh_ingredient_count(fresh_ranges, ingredient_ids):
    def is_fresh(id):
        for min, max in fresh_ranges:
            if min <= id <= max:
                return True
        return False

    return sum(is_fresh(id) for id in ingredient_ids)


def run_program(input):
    fresh_ranges, ingredient_ids = parse_input(input)
    return get_fresh_ingredient_count(fresh_ranges, ingredient_ids)


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

            1
            5
            8
            11
            17
            32
            """
        )

        result = run_program(input)

        self.assertEqual(result, 3)
