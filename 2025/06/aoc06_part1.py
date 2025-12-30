#
# Advent of Code 2025, day 06, part 1
#

import collections
import functools
import operator
import textwrap
import unittest


def read_input():
    with open("input", encoding="utf-8") as f:
        return f.read()


def parse_input(input):
    # Returns a list of problems of the form [n1, n2, ..., op].
    problems = collections.defaultdict(list)

    lines = input.strip().split("\n")
    for line in lines[:-1]:
        for i, n in enumerate(line.split()):
            problems[i].append(int(n))

    for i, op in enumerate(lines[-1].split()):
        problems[i].append(operator.add if op == "+" else operator.mul)

    return list(problems.values())


def run_program(input):
    problems = parse_input(input)
    return sum(functools.reduce(p[-1], p[:-1]) for p in problems)


if __name__ == "__main__":
    result = run_program(read_input())
    print(result)


class Tests(unittest.TestCase):
    def test_program_returns_correct_result_for_example_input(self):
        input = textwrap.dedent(
            """
            123 328  51 64
             45 64  387 23
              6 98  215 314
            *   +   *   +
            """
        )

        result = run_program(input)

        self.assertEqual(result, 4277556)
