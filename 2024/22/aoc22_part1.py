#
# Advent of Code 2024, day 22, part 1
#

import textwrap
import unittest


def read_input():
    with open("input", encoding="utf-8") as f:
        return f.read()


def parse_input(input):
    return [int(n) for n in input.strip().split("\n")]


def evolve_secret_number(n, turn_count):
    def mix(m):
        return n ^ m

    def prune(m):
        return m % 16777216

    for _ in range(turn_count):
        n = prune(mix(n * 64))
        n = prune(mix(n // 32))
        n = prune(mix(n * 2048))
    return n


def run_program(input, turn_count=2000):
    secret_numbers = parse_input(input)
    return sum(
        evolve_secret_number(secret_number, turn_count)
        for secret_number in secret_numbers
    )


if __name__ == "__main__":
    result = run_program(read_input())
    print(result)


class Tests(unittest.TestCase):
    def test_program_returns_correct_result_for_example_input(self):
        input = textwrap.dedent(
            """
            1
            10
            100
            2024
            """
        )

        result = run_program(input)

        self.assertEqual(result, 37327623)
