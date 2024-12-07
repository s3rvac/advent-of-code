#
# Advent of Code 2024, day 07, part 2
#

import dataclasses
import functools
import itertools
import textwrap
import unittest


@dataclasses.dataclass
class Equation:
    test_value: int
    operands: list[int]


def read_input():
    with open("input", encoding="utf-8") as f:
        return f.read()


def parse_input(input):
    def parse_equation(eq):
        lhs, rhs = eq.split(": ")
        return Equation(int(lhs), [int(n) for n in rhs.strip().split(" ")])

    return [parse_equation(line) for line in input.strip("\n").split("\n")]


def is_solvable_equation(eq):
    def reducer_for(operators):
        operators = iter(operators)

        def reduce(x, y):
            match next(operators):
                case "+":
                    return x + y
                case "*":
                    return x * y
                case "||":
                    return int(str(x) + str(y))

        return reduce

    possibilities = itertools.product(["+", "*", "||"], repeat=len(eq.operands) - 1)
    for operators in possibilities:
        result = functools.reduce(reducer_for(operators), eq.operands)
        if result == eq.test_value:
            return True
    return False


def run_program(input):
    equations = parse_input(input)
    return sum(eq.test_value for eq in equations if is_solvable_equation(eq))


if __name__ == "__main__":
    result = run_program(read_input())
    print(result)


class Tests(unittest.TestCase):
    def test_program_returns_correct_result_for_example_input(self):
        input = textwrap.dedent(
            """
            190: 10 19
            3267: 81 40 27
            83: 17 5
            156: 15 6
            7290: 6 8 6 15
            161011: 16 10 13
            192: 17 8 14
            21037: 9 7 18 13
            292: 11 6 16 20
            """
        )

        result = run_program(input)

        self.assertEqual(result, 11387)
