#
# Advent of Code 2024, day 03, part 1
#

import re
import textwrap
import unittest


def read_input():
    with open("input", encoding="utf-8") as f:
        return f.read()


def parse_input(input):
    return input.strip()


def get_mul_instructions(memory):
    return [(int(a), int(b)) for a, b in re.findall(r"mul\((\d+),(\d+)\)", memory)]


def run_program(input):
    memory = parse_input(input)
    mul_instructions = get_mul_instructions(memory)
    return sum(a * b for a, b in mul_instructions)


if __name__ == "__main__":
    result = run_program(read_input())
    print(result)


class Tests(unittest.TestCase):
    def test_program_returns_correct_result_for_example_input(self):
        input = textwrap.dedent(
            """
            xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))
            """
        )

        result = run_program(input)

        self.assertEqual(result, 161)
