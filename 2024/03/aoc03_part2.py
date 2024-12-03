#
# Advent of Code 2024, day 03, part 2
#

import re
import textwrap
import unittest


def read_input():
    with open("input", encoding="utf-8") as f:
        return f.read()


def parse_input(input):
    return input.strip()


def get_enabled_mul_instructions(memory):
    # Whether processing of instructions is enabled or not. At the beginning,
    # it is enabled.
    enabled = True

    mul_instructions = []
    for instr in re.findall(r"do\(\)|don't\(\)|mul\(\d+,\d+\)", memory):
        if instr == "do()":
            enabled = True
        elif instr == "don't()":
            enabled = False
        elif enabled:
            m = re.match(r"mul\((\d+),(\d+)\)", instr)
            assert m is not None
            mul_instructions.append((int(m.group(1)), int(m.group(2))))
    return mul_instructions


def run_program(input):
    memory = parse_input(input)
    mul_instructions = get_enabled_mul_instructions(memory)
    return sum(a * b for a, b in mul_instructions)


if __name__ == "__main__":
    result = run_program(read_input())
    print(result)


class Tests(unittest.TestCase):
    def test_program_returns_correct_result_for_example_input(self):
        input = textwrap.dedent(
            """
            xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))
            """
        )

        result = run_program(input)

        self.assertEqual(result, 48)
