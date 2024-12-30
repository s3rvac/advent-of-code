#
# Advent of Code 2023, day 08, part 1
#

import re
import textwrap
import unittest


def read_input():
    with open("input", encoding="utf-8") as f:
        return f.read()


def parse_input(input):
    lines = input.strip().split("\n")

    instructions = list(lines[0])

    network = {}
    for line in lines[2:]:
        m = re.fullmatch(r"(.+) = \((.+), (.+)\)", line)
        assert m is not None
        current_node, left_node, right_node = m.groups()
        network[current_node] = {"L": left_node, "R": right_node}

    return instructions, network


def count_steps_to_reach_end_node(instructions, network):
    steps = 0
    node = "AAA"
    while node != "ZZZ":
        node = network[node][instructions[steps % len(instructions)]]
        steps += 1
    return steps


def run_program(input):
    instructions, network = parse_input(input)
    return count_steps_to_reach_end_node(instructions, network)


if __name__ == "__main__":
    result = run_program(read_input())
    print(result)


class Tests(unittest.TestCase):
    def test_program_returns_correct_result_for_example_input(self):
        input = textwrap.dedent(
            """
            LLR

            AAA = (BBB, BBB)
            BBB = (AAA, ZZZ)
            ZZZ = (ZZZ, ZZZ)
            """
        )

        result = run_program(input)

        self.assertEqual(result, 6)
