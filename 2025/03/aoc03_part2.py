#
# Advent of Code 2025, day 03, part 2
#

import functools
import textwrap
import unittest


def read_input():
    with open("input", encoding="utf-8") as f:
        return f.read()


def parse_input(input):
    return [line for line in input.strip().split()]


def get_largest_joltage(bank):
    @functools.cache
    def max_from(i, remaining):
        if remaining == 0 or i >= len(bank):
            return 0

        # If we only have one remaining digit left, try going with the current
        # digit.
        m1 = int(bank[i]) if remaining == 1 else 0

        # Try skipping the current digit.
        m2 = max_from(i + 1, remaining)

        # Try using the current digit.
        m3 = max_from(i + 1, remaining - 1)
        if m3 != 0:
            m3 = int(f"{bank[i]}{m3}")

        return max(m1, m2, m3)

    return max_from(i=0, remaining=12)


def run_program(input):
    banks = parse_input(input)
    return sum(get_largest_joltage(bank) for bank in banks)


if __name__ == "__main__":
    result = run_program(read_input())
    print(result)


class Tests(unittest.TestCase):
    def test_program_returns_correct_result_for_example_input(self):
        input = textwrap.dedent(
            """
            987654321111111
            811111111111119
            234234234234278
            818181911112111
            """
        )

        result = run_program(input)

        self.assertEqual(result, 3121910778619)
