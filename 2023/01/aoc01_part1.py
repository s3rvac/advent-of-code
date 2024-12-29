#
# Advent of Code 2023, day 01, part 1
#

import textwrap
import unittest


def read_input():
    with open("input", encoding="utf-8") as f:
        return f.read()


def parse_input(input):
    return list(input.strip().split("\n"))


def compute_calibration_values(lines):
    return list(map(compute_calibration_value, lines))


def compute_calibration_value(line):
    digits = list(filter(lambda c: c.isdigit(), line))
    return int(digits[0] + digits[-1])


def run_program(input):
    lines = parse_input(input)
    return sum(compute_calibration_values(lines))


if __name__ == "__main__":
    result = run_program(read_input())
    print(result)


class Tests(unittest.TestCase):
    def test_program_returns_correct_result_for_example_input(self):
        input = textwrap.dedent(
            """
            1abc2
            pqr3stu8vwx
            a1b2c3d4e5f
            treb7uchet
            """
        )

        result = run_program(input)

        self.assertEqual(result, 142)
