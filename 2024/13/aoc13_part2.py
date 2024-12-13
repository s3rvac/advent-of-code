#
# Advent of Code 2024, day 13, part 2
#

import dataclasses
import re
import textwrap
import unittest


BUTTON_A_COST = 3
BUTTON_B_COST = 1
PRIZE_INCREMENT = 10000000000000


@dataclasses.dataclass
class Machine:
    a_x: int
    a_y: int
    b_x: int
    b_y: int
    prize_x: int
    prize_y: int


def read_input():
    with open("input", encoding="utf-8") as f:
        return f.read()


def parse_input(input):
    def parse_machine(raw_machine):
        l1, l2, l3 = raw_machine.split("\n")

        m1 = re.match(r"Button A: X\+(\d+), Y\+(\d+)", l1)
        assert m1 is not None
        a_x, a_y = m1.groups()

        m2 = re.match(r"Button B: X\+(\d+), Y\+(\d+)", l2)
        assert m2 is not None
        b_x, b_y = m2.groups()

        m3 = re.match(r"Prize: X=(\d+), Y=(\d+)", l3)
        assert m3 is not None
        prize_x, prize_y = m3.groups()

        return Machine(
            a_x=int(a_x),
            a_y=int(a_y),
            b_x=int(b_x),
            b_y=int(b_y),
            prize_x=int(prize_x) + PRIZE_INCREMENT,
            prize_y=int(prize_y) + PRIZE_INCREMENT,
        )

    return list(map(parse_machine, input.strip().split("\n\n")))


def get_cheapest_cost_of_winning_prize_for_machine(m):
    # We solve the following system of two linear equations via variable
    # elimination and check that the resulting numbers are integers (the number
    # of button presses cannot be decimal).
    #
    #     A * a_x + B * b_x = prize_x
    #     A * a_y + B * b_y = prize_y
    #
    B = (m.prize_x * m.a_y - m.prize_y * m.a_x) / (m.b_x * m.a_y - m.a_x * m.b_y)
    A = (m.prize_x - B * m.b_x) / m.a_x
    if not A.is_integer() or not B.is_integer():
        return 0
    return BUTTON_A_COST * int(A) + BUTTON_B_COST * int(B)


def run_program(input):
    machines = parse_input(input)
    return sum(map(get_cheapest_cost_of_winning_prize_for_machine, machines))


if __name__ == "__main__":
    result = run_program(read_input())
    print(result)


class Tests(unittest.TestCase):
    def test_program_returns_correct_result_for_example_input(self):
        input = textwrap.dedent(
            """
            Button A: X+94, Y+34
            Button B: X+22, Y+67
            Prize: X=8400, Y=5400

            Button A: X+26, Y+66
            Button B: X+67, Y+21
            Prize: X=12748, Y=12176

            Button A: X+17, Y+86
            Button B: X+84, Y+37
            Prize: X=7870, Y=6450

            Button A: X+69, Y+23
            Button B: X+27, Y+71
            Prize: X=18641, Y=10279
            """
        )

        result = run_program(input)

        self.assertEqual(result, 875318608908)
