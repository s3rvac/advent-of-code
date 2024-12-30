#
# Advent of Code 2023, day 06, part 1
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
    times = [int(n) for n in re.findall(r"\d+", lines[0])]
    record_distances = [int(n) for n in re.findall(r"\d+", lines[1])]
    return times, record_distances


def compute_number_of_ways_to_beat_record(time, record_distance):
    way_count = 0
    for n in range(1, time):
        distance = n * (time - n)
        if distance > record_distance:
            way_count += 1
    return way_count


def run_program(input):
    times, record_distances = parse_input(input)
    return math.prod(
        compute_number_of_ways_to_beat_record(time, record_distance)
        for time, record_distance in zip(times, record_distances)
    )


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

        self.assertEqual(result, 288)
