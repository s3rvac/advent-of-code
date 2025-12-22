#
# Advent of Code 2025, day 01, part 1
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
    password = 0

    c = 50
    for dir, n in rotations:
        op = operator.add if dir == "R" else operator.sub
        c = op(c, n) % 100
        if c == 0:
            password += 1

    return password


def run_program(input):
    rotations = parse_input(input)
    return get_password(rotations)


if __name__ == "__main__":
    result = run_program(read_input())
    print(result)


class Tests(unittest.TestCase):
    def test_program_returns_correct_result_for_example_input(self):
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

        self.assertEqual(result, 3)
