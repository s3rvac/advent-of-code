#
# Advent of Code 2023, day 08, part 2
#

import math
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
        current_node, left_node, right_node = m.groups()
        network[current_node] = {"L": left_node, "R": right_node}

    return instructions, network


def count_steps_to_reach_terminal_nodes(instructions, network):
    # Gist: For each node ending with A, compute the number of steps that it
    # takes to arrive at a node ending with Z. Then, compute the least common
    # multiple of those steps, which gives us the total number of steps after
    # which we arrive at all Z nodes at the same time.
    required_steps_for_each_a_node = []
    a_nodes = {node for node in network if node.endswith("A")}
    for node in a_nodes:
        i = 0
        steps = 0
        while not node.endswith("Z"):
            node = network[node][instructions[i]]
            steps += 1
            i = (i + 1) % len(instructions)
        required_steps_for_each_a_node.append(steps)
    return math.lcm(*required_steps_for_each_a_node)


def run_program(input):
    instructions, network = parse_input(input)
    return count_steps_to_reach_terminal_nodes(instructions, network)


if __name__ == "__main__":
    result = run_program(read_input())
    print(result)


class Tests(unittest.TestCase):
    def test_program_returns_correct_result_for_example_input(self):
        input = textwrap.dedent(
            """
            LR

            11A = (11B, XXX)
            11B = (XXX, 11Z)
            11Z = (11B, XXX)
            22A = (22B, XXX)
            22B = (22C, 22C)
            22C = (22Z, 22Z)
            22Z = (22B, 22B)
            XXX = (XXX, XXX)
            """
        )

        result = run_program(input)

        self.assertEqual(result, 6)
