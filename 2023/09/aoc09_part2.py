#
# Advent of Code 2023, day 09, part 2
#

import itertools
import textwrap
import unittest


def read_input():
    with open("input", encoding="utf-8") as f:
        return f.read()


def parse_input(input):
    return [[int(n) for n in line.split(" ")] for line in input.strip().split("\n")]


def find_previous_value_for_history(history):
    sequences = [history]
    while any(sequences[-1]):
        sequences.append([b - a for a, b in itertools.pairwise(sequences[-1])])

    previous_value = 0
    for seq in reversed(sequences):
        previous_value = seq[0] - previous_value
    return previous_value


def run_program(input):
    histories = parse_input(input)
    return sum(map(find_previous_value_for_history, histories))


if __name__ == "__main__":
    result = run_program(read_input())
    print(result)


class Tests(unittest.TestCase):
    def test_program_returns_correct_result_for_example_input(self):
        input = textwrap.dedent(
            """
            0 3 6 9 12 15
            1 3 6 10 15 21
            10 13 16 21 30 45
            """
        )

        result = run_program(input)

        self.assertEqual(result, 2)
