#
# Advent of Code 2025, day 10, part 2
#
# Requirements:
#
#     pip install z3-solver==4.15.4.0
#

import dataclasses
import re
import textwrap
import unittest

import z3


@dataclasses.dataclass
class Machine:
    buttons: list[list[int]]
    joltage_config: list[int]

    def get_init_joltage_config(self):
        return [0] * len(self.joltage_config)


def read_input():
    with open("input", encoding="utf-8") as f:
        return f.read()


def parse_input(input):
    def parse_machine(raw_machine):
        m = re.fullmatch(r"\[[\.#]+\] (.+) \{(.*)\}", raw_machine)
        assert m is not None
        buttons = [
            list(map(int, raw_buttons.strip("()").split(",")))
            for raw_buttons in m.group(1).split(" ")
        ]
        joltage_config = list(map(int, m.group(2).split(",")))
        return Machine(buttons, joltage_config)

    return [parse_machine(line) for line in input.strip().split("\n")]


def get_fewest_bpress_count_to_configure_joltages(machine):
    # Use the Z3 solver to optimize (minimize) the number of button presses by
    # solving the provided constraints that define the machine.
    s = z3.Optimize()

    z3_buttons = {z3.Int(f"b{i}"): b for i, b in enumerate(machine.buttons)}

    # Define the constraints:
    #
    #   1. The number of button presses cannot be negative. E.g. for the first
    #   machine in the provided example in the assignment:
    #
    #          b0 >= 0
    #          b1 >= 0
    #          ...
    #          b5 >= 0
    #
    for b in z3_buttons:
        s.add(b >= 0)

    #   2. The sum of the button presses (left-hand side of the constraint) has
    #      to be equal to the expected joltage (right-hand side of the
    #      constraint). E.g. for the first machine in the provided example in
    #      the assignment:
    #
    #          b4 + b5      == 3
    #          b1 + b5      == 5
    #          b2 + b3 + b4 == 4
    #          b0 + b1 + b3 == 7
    #
    for i, joltage in enumerate(machine.joltage_config):
        lhs = 0
        for z3b, b in z3_buttons.items():
            for _ in [x for x in b if x == i]:
                lhs += z3b
        s.add(lhs == joltage)

    # Find the minimal number of button presses that satisfy the constraints
    # above.
    bpress = z3.Int("bpress")
    s.add(bpress == sum(z3_buttons))
    s.minimize(bpress)
    s.check()
    result = s.model()[bpress]
    assert isinstance(result, z3.IntNumRef)
    return result.as_long()


def run_program(input):
    machines = parse_input(input)
    return sum(map(get_fewest_bpress_count_to_configure_joltages, machines))


if __name__ == "__main__":
    result = run_program(read_input())
    print(result)


class Tests(unittest.TestCase):
    def test_program_returns_correct_result_for_example_input(self):
        input = textwrap.dedent(
            """
            [.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
            [...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}
            [.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}
            """
        )

        result = run_program(input)

        self.assertEqual(result, 33)
