#
# Advent of Code 2023, day 06, part 2
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
    time = "".join(re.findall(r"\d+", lines[0]))
    record_distance = "".join(re.findall(r"\d+", lines[1]))
    return int(time), int(record_distance)


def compute_number_of_ways_to_beat_record(time, record_distance):
    # The input time is too big in the second part, so instead of checking all
    # the possibilities, just solve an equation that gives the answers. In this
    # case, we are trying to find all `n` that satisfy
    #
    #    n * (time - n) > record_distance
    #
    # After rewriting the equation, we get
    #
    #    n * (time - n) - record_distance == 0
    #    n * time - n**2 - record_distance == 0
    #    -n**2 + n * time - record_distance == 0
    #
    # The equation can be solved via the quadratic formula, which gives us the
    # lower and upper bounds for when we get exactly the record distance.
    # Anything in between counts as a way of beating the record.
    discriminant = time**2 - 4 * record_distance
    n1 = (-time + math.isqrt(discriminant)) / -2
    n2 = (-time - math.isqrt(discriminant)) / -2
    return math.floor(n2) - math.ceil(n1) + 1


def run_program(input):
    time, record_distance = parse_input(input)
    return compute_number_of_ways_to_beat_record(time, record_distance)


if __name__ == "__main__":
    result = run_program(read_input())
    print(result)


class Tests(unittest.TestCase):
    def test_program_returns_correct_result_for_example_input(self):
        input = textwrap.dedent(
            """
            Time:      7  15   30
            Distance:  9  40  200
            """
        )

        result = run_program(input)

        self.assertEqual(result, 71503)
