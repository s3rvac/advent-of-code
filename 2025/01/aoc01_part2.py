#
# Advent of Code 2025, day 01, part 2
#

import operator
import textwrap
import unittest


def read_input():
    with open("input", encoding="utf-8") as f:
        return f.read()


def parse_input(input):
    return [(line[0], int(line[1:])) for line in input.strip().split("\n")]


def get_password(rotations):
    # The password is the number of times the dial points at 0, regardless of
    # whether it happens during a rotation or at the end of one.
    password = 0

    c = 50
    for dir, n in rotations:
        password += n // 100
        n %= 100
        op = operator.add if dir == "R" else operator.sub
        x = op(c, n)
        if (c != 0 and x <= 0) or x >= 100:
            password += 1
        c = x % 100

    return password


def run_program(input):
    rotations = parse_input(input)
    return get_password(rotations)


if __name__ == "__main__":
    result = run_program(read_input())
    print(result)


class Tests(unittest.TestCase):
    def test_program_returns_correct_result_for_example_input1(self):
        input = textwrap.dedent(
            """
            L68
            L30
            R48
            L5
            R60
            L55
            L1
            L99
            R14
            L82
            """
        )

        result = run_program(input)

        self.assertEqual(result, 6)

    def test_program_returns_correct_result_for_example_input2(self):
        input = textwrap.dedent(
            """
            R1000
            """
        )

        result = run_program(input)

        self.assertEqual(result, 10)
