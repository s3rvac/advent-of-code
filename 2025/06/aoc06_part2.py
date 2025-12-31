#
# Advent of Code 2025, day 06, part 2
#

import functools
import operator
import textwrap
import unittest


def read_input():
    with open("input", encoding="utf-8") as f:
        return f.read()


def parse_input(input):
    # Returns a list of problems of the form [n1, n2, ..., op].
    problems = []

    lines = input.strip().split("\n")

    # Get the start and end index (column) for each problem by utilizing the fact that
    # each operator is in the leftmost column for each problem.
    start_indexes = []
    for i, c in enumerate(lines[-1]):
        if c in ("+", "*"):
            start_indexes.append(i)
        i += 1
    end_indexes = start_indexes[1:] + [len(lines[0]) + 2]

    # Parse the problems utilizing the start and end indexes.
    for i, j in zip(start_indexes, end_indexes):
        raw_problem = [line[i : j - 1] for line in lines[:-1]]
        problem = []
        for k in range(len(raw_problem[0]), 0, -1):
            problem.append(int("".join(num[k - 1] for num in raw_problem).strip()))
        problems.append(problem)

    # Add an operator to the end of each problem.
    for i, op in enumerate(lines[-1].split()):
        problems[i].append(operator.add if op == "+" else operator.mul)

    return problems


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
            123 328  51 64#
             45 64  387 23#
              6 98  215 314
            *   +   *   +
            """
        ).replace("#", " ")

        result = run_program(input)

        self.assertEqual(result, 3263827)
