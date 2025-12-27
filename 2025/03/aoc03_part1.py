#
# Advent of Code 2025, day 03, part 1
#

import textwrap
import unittest


def read_input():
    with open("input", encoding="utf-8") as f:
        return f.read()


def parse_input(input):
    return [line for line in input.strip().split()]


def get_largest_joltage(bank):
    for j1 in range(9, 0, -1):
        i = bank.find(str(j1))
        if 0 <= i < len(bank) - 1:
            j2 = max(int(x) for x in bank[i + 1 :])
            return j1 * 10 + j2
    raise AssertionError("invalid bank")


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

        self.assertEqual(result, 357)
