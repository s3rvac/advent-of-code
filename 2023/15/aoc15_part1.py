#
# Advent of Code 2023, day 15, part 1
#

import textwrap
import unittest


def read_input():
    with open("input", encoding="utf-8") as f:
        return f.read()


def parse_input(input):
    return input.strip("\n").split(",")


def hash_string(string):
    hash = 0
    for c in string:
        hash = ((hash + ord(c)) * 17) % 256
    return hash


def run_program(input):
    initialization_sequence = parse_input(input)
    return sum(map(hash_string, initialization_sequence))


if __name__ == "__main__":
    result = run_program(read_input())
    print(result)


class Tests(unittest.TestCase):
    def test_program_returns_correct_result_for_example_input(self):
        input = textwrap.dedent(
            """
            rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7
            """
        )

        result = run_program(input)

        self.assertEqual(result, 1320)
